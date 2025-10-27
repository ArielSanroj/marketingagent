"""
Comprehensive tests for the rate limiting system
"""
import pytest
import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from utils.rate_limiter import (
    RateLimitRule, RateLimitAlgorithm, ThreatLevel, ClientInfo,
    TokenBucket, SlidingWindow, LeakyBucket, RateLimiter,
    DDoSProtection, SecurityHeaders, get_rate_limiter, get_ddos_protection,
    check_rate_limit, analyze_request_pattern
)

class TestRateLimitRule:
    """Test RateLimitRule functionality"""
    
    def test_rate_limit_rule_initialization(self):
        """Test rate limit rule initialization"""
        rule = RateLimitRule()
        
        assert rule.requests_per_minute == 60
        assert rule.requests_per_hour == 1000
        assert rule.requests_per_day == 10000
        assert rule.burst_limit == 10
        assert rule.algorithm == RateLimitAlgorithm.SLIDING_WINDOW
        assert rule.block_duration_seconds == 300
        assert rule.whitelist is None
        assert rule.blacklist is None
    
    def test_rate_limit_rule_with_custom_values(self):
        """Test rate limit rule with custom values"""
        rule = RateLimitRule(
            requests_per_minute=120,
            requests_per_hour=2000,
            requests_per_day=20000,
            burst_limit=20,
            algorithm=RateLimitAlgorithm.TOKEN_BUCKET,
            block_duration_seconds=600,
            whitelist=["192.168.1.1"],
            blacklist=["10.0.0.1"]
        )
        
        assert rule.requests_per_minute == 120
        assert rule.requests_per_hour == 2000
        assert rule.requests_per_day == 20000
        assert rule.burst_limit == 20
        assert rule.algorithm == RateLimitAlgorithm.TOKEN_BUCKET
        assert rule.block_duration_seconds == 600
        assert rule.whitelist == ["192.168.1.1"]
        assert rule.blacklist == ["10.0.0.1"]

class TestClientInfo:
    """Test ClientInfo functionality"""
    
    def test_client_info_initialization(self):
        """Test client info initialization"""
        now = datetime.now()
        client = ClientInfo(
            ip_address="192.168.1.1",
            user_agent="test_agent",
            first_seen=now,
            last_request=now
        )
        
        assert client.ip_address == "192.168.1.1"
        assert client.user_agent == "test_agent"
        assert client.first_seen == now
        assert client.last_request == now
        assert client.request_count == 0
        assert client.blocked_until is None
        assert client.threat_level == ThreatLevel.LOW
        assert client.violations == 0

class TestTokenBucket:
    """Test TokenBucket functionality"""
    
    def test_token_bucket_initialization(self):
        """Test token bucket initialization"""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)
        
        assert bucket.capacity == 10
        assert bucket.tokens == 10
        assert bucket.refill_rate == 1.0
    
    def test_token_bucket_consume_success(self):
        """Test successful token consumption"""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)
        
        result = bucket.consume(5)
        
        assert result is True
        assert bucket.tokens == 5
    
    def test_token_bucket_consume_insufficient_tokens(self):
        """Test token consumption with insufficient tokens"""
        bucket = TokenBucket(capacity=5, refill_rate=1.0)
        
        result = bucket.consume(10)
        
        assert result is False
        assert bucket.tokens == 5
    
    def test_token_bucket_refill(self):
        """Test token bucket refill over time"""
        bucket = TokenBucket(capacity=10, refill_rate=1.0)
        bucket.tokens = 5
        
        # Simulate time passing
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0, 2]  # 2 seconds later
            result = bucket.consume(3)
            
            assert result is True
            assert bucket.tokens == 4  # 5 + 2*1.0 - 3 = 4
    
    def test_token_bucket_capacity_limit(self):
        """Test token bucket capacity limit"""
        bucket = TokenBucket(capacity=5, refill_rate=10.0)
        bucket.tokens = 0
        
        # Simulate time passing
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0, 1]  # 1 second later
            result = bucket.consume(3)
            
            assert result is True
            assert bucket.tokens == 2  # min(5, 0 + 1*10.0) - 3 = 2

class TestSlidingWindow:
    """Test SlidingWindow functionality"""
    
    def test_sliding_window_initialization(self):
        """Test sliding window initialization"""
        window = SlidingWindow(window_size=60, max_requests=10)
        
        assert window.window_size == 60
        assert window.max_requests == 10
        assert len(window.requests) == 0
    
    def test_sliding_window_allowed(self):
        """Test sliding window when request is allowed"""
        window = SlidingWindow(window_size=60, max_requests=5)
        
        # First 5 requests should be allowed
        for i in range(5):
            result = window.is_allowed()
            assert result is True
        
        # 6th request should be denied
        result = window.is_allowed()
        assert result is False
    
    def test_sliding_window_old_requests_removal(self):
        """Test removal of old requests from window"""
        window = SlidingWindow(window_size=60, max_requests=2)
        
        # Add requests
        with patch('time.time', return_value=100):
            window.is_allowed()  # First request
            window.is_allowed()  # Second request
        
        # Third request should be denied
        with patch('time.time', return_value=100):
            result = window.is_allowed()
            assert result is False
        
        # After window expires, requests should be allowed again
        with patch('time.time', return_value=200):  # 100 seconds later
            result = window.is_allowed()
            assert result is True

class TestLeakyBucket:
    """Test LeakyBucket functionality"""
    
    def test_leaky_bucket_initialization(self):
        """Test leaky bucket initialization"""
        bucket = LeakyBucket(capacity=10, leak_rate=1.0)
        
        assert bucket.capacity == 10
        assert bucket.tokens == 0
        assert bucket.leak_rate == 1.0
    
    def test_leaky_bucket_add_request_success(self):
        """Test successful request addition"""
        bucket = LeakyBucket(capacity=10, leak_rate=1.0)
        
        result = bucket.add_request()
        
        assert result is True
        assert bucket.tokens == 1
    
    def test_leaky_bucket_add_request_capacity_full(self):
        """Test request addition when capacity is full"""
        bucket = LeakyBucket(capacity=2, leak_rate=0.5)
        bucket.tokens = 2  # Fill to capacity
        
        result = bucket.add_request()
        
        assert result is False
        assert bucket.tokens == 2
    
    def test_leaky_bucket_leak_tokens(self):
        """Test token leaking over time"""
        bucket = LeakyBucket(capacity=10, leak_rate=2.0)
        bucket.tokens = 5
        
        # Simulate time passing
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0, 1]  # 1 second later
            result = bucket.add_request()
            
            assert result is True
            assert bucket.tokens == 4  # 5 - 1*2.0 + 1 = 4

class TestRateLimiter:
    """Test RateLimiter functionality"""
    
    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization"""
        rule = RateLimitRule()
        limiter = RateLimiter(rule)
        
        assert limiter.default_rule == rule
        assert len(limiter.clients) == 0
        assert len(limiter.rate_limiters) == 0
        assert len(limiter.blocked_ips) == 0
    
    def test_get_client_key(self):
        """Test client key generation"""
        rule = RateLimitRule()
        limiter = RateLimiter(rule)
        
        key1 = limiter._get_client_key("192.168.1.1", "agent1")
        key2 = limiter._get_client_key("192.168.1.1", "agent1")
        key3 = limiter._get_client_key("192.168.1.1", "agent2")
        
        assert key1 == key2
        assert key1 != key3
    
    def test_update_client_info(self):
        """Test client info update"""
        rule = RateLimitRule()
        limiter = RateLimiter(rule)
        
        limiter._update_client_info("192.168.1.1", "agent1", "client_key")
        
        assert "client_key" in limiter.clients
        client = limiter.clients["client_key"]
        assert client.ip_address == "192.168.1.1"
        assert client.user_agent == "agent1"
        assert client.request_count == 1
    
    def test_assess_threat_level_low(self):
        """Test threat level assessment for low threat"""
        rule = RateLimitRule()
        limiter = RateLimiter(rule)
        
        # Create client with low activity
        client_key = "test_client"
        limiter.clients[client_key] = ClientInfo(
            ip_address="192.168.1.1",
            user_agent="agent1",
            first_seen=datetime.now(),
            last_request=datetime.now(),
            request_count=10,
            violations=0
        )
        
        threat_level = limiter._assess_threat_level(client_key)
        assert threat_level == ThreatLevel.LOW
    
    def test_assess_threat_level_high(self):
        """Test threat level assessment for high threat"""
        rule = RateLimitRule()
        limiter = RateLimiter(rule)
        
        # Create client with high activity
        client_key = "test_client"
        limiter.clients[client_key] = ClientInfo(
            ip_address="192.168.1.1",
            user_agent="agent1",
            first_seen=datetime.now(),
            last_request=datetime.now(),
            request_count=1000,  # High request count
            violations=6  # High violation count
        )
        
        threat_level = limiter._assess_threat_level(client_key)
        assert threat_level == ThreatLevel.HIGH
    
    def test_is_allowed_whitelisted_ip(self):
        """Test allowing whitelisted IP"""
        rule = RateLimitRule(whitelist=["192.168.1.1"])
        limiter = RateLimiter(rule)
        
        allowed, reason, details = limiter.is_allowed("192.168.1.1", "agent1")
        
        assert allowed is True
        assert reason == "Whitelisted"
        assert details == {}
    
    def test_is_allowed_blacklisted_ip(self):
        """Test blocking blacklisted IP"""
        rule = RateLimitRule(blacklist=["192.168.1.1"])
        limiter = RateLimiter(rule)
        
        allowed, reason, details = limiter.is_allowed("192.168.1.1", "agent1")
        
        assert allowed is False
        assert reason == "Blacklisted"
        assert "192.168.1.1" in limiter.blocked_ips
    
    def test_is_allowed_blocked_ip(self):
        """Test blocking already blocked IP"""
        rule = RateLimitRule()
        limiter = RateLimiter(rule)
        
        # Block IP
        limiter.blocked_ips["192.168.1.1"] = datetime.now() + timedelta(minutes=5)
        
        allowed, reason, details = limiter.is_allowed("192.168.1.1", "agent1")
        
        assert allowed is False
        assert reason == "IP blocked"
        assert "blocked_until" in details
    
    def test_is_allowed_rate_limit_exceeded(self):
        """Test rate limit exceeded scenario"""
        rule = RateLimitRule(requests_per_minute=1)  # Very low limit
        limiter = RateLimiter(rule)
        
        # First request should be allowed
        allowed, reason, details = limiter.is_allowed("192.168.1.1", "agent1")
        assert allowed is True
        
        # Second request should be blocked
        allowed, reason, details = limiter.is_allowed("192.168.1.1", "agent1")
        assert allowed is False
        assert reason == "Rate limit exceeded"
    
    def test_block_ip(self):
        """Test IP blocking functionality"""
        rule = RateLimitRule()
        limiter = RateLimiter(rule)
        
        limiter._block_ip("192.168.1.1", "Test blocking")
        
        assert "192.168.1.1" in limiter.blocked_ips
        blocked_until = limiter.blocked_ips["192.168.1.1"]
        assert blocked_until > datetime.now()
    
    def test_get_stats(self):
        """Test getting rate limiter statistics"""
        rule = RateLimitRule()
        limiter = RateLimiter(rule)
        
        # Add some test data
        limiter.clients["client1"] = ClientInfo(
            ip_address="192.168.1.1",
            user_agent="agent1",
            first_seen=datetime.now(),
            last_request=datetime.now(),
            request_count=10,
            threat_level=ThreatLevel.LOW
        )
        limiter.clients["client2"] = ClientInfo(
            ip_address="192.168.1.2",
            user_agent="agent2",
            first_seen=datetime.now(),
            last_request=datetime.now(),
            request_count=5,
            threat_level=ThreatLevel.HIGH
        )
        limiter.blocked_ips["192.168.1.3"] = datetime.now() + timedelta(minutes=5)
        
        stats = limiter.get_stats()
        
        assert stats['active_clients'] == 2
        assert stats['blocked_ips'] == 1
        assert stats['threat_level_distribution']['low'] == 1
        assert stats['threat_level_distribution']['high'] == 1
        assert stats['total_requests'] == 15
        assert stats['average_requests_per_client'] == 7.5

class TestDDoSProtection:
    """Test DDoSProtection functionality"""
    
    def test_ddos_protection_initialization(self):
        """Test DDoS protection initialization"""
        rate_limiter = MagicMock()
        ddos_protection = DDoSProtection(rate_limiter)
        
        assert ddos_protection.rate_limiter == rate_limiter
        assert ddos_protection.attack_detection_threshold == 100
        assert len(ddos_protection.suspicious_patterns) == 0
    
    def test_analyze_request_pattern_normal(self):
        """Test analyzing normal request pattern"""
        rate_limiter = MagicMock()
        ddos_protection = DDoSProtection(rate_limiter)
        
        allowed, reason = ddos_protection.analyze_request_pattern(
            "192.168.1.1", "agent1", "/test"
        )
        
        assert allowed is True
        assert reason == "Pattern analysis passed"
        assert ddos_protection.suspicious_patterns["192.168.1.1:/test"] == 1
    
    def test_analyze_request_pattern_attack(self):
        """Test analyzing attack request pattern"""
        rate_limiter = MagicMock()
        ddos_protection = DDoSProtection(rate_limiter)
        
        # Simulate many requests from same IP to same endpoint
        for i in range(101):  # Exceed threshold
            allowed, reason = ddos_protection.analyze_request_pattern(
                "192.168.1.1", "agent1", "/test"
            )
        
        assert allowed is False
        assert reason == "DDoS attack detected"
    
    def test_get_attack_stats(self):
        """Test getting attack statistics"""
        rate_limiter = MagicMock()
        ddos_protection = DDoSProtection(rate_limiter)
        
        # Add some suspicious patterns
        ddos_protection.suspicious_patterns["192.168.1.1:/test"] = 50
        ddos_protection.suspicious_patterns["192.168.1.2:/api"] = 30
        
        stats = ddos_protection.get_attack_stats()
        
        assert stats['suspicious_patterns'] == 2
        assert stats['total_suspicious_requests'] == 80
        assert len(stats['top_attackers']) == 2
        assert stats['top_attackers'][0][0] == "192.168.1.1:/test"
        assert stats['top_attackers'][0][1] == 50

class TestSecurityHeaders:
    """Test SecurityHeaders functionality"""
    
    def test_get_security_headers(self):
        """Test getting security headers"""
        headers = SecurityHeaders.get_security_headers()
        
        assert 'X-Content-Type-Options' in headers
        assert 'X-Frame-Options' in headers
        assert 'X-XSS-Protection' in headers
        assert 'Strict-Transport-Security' in headers
        assert 'Content-Security-Policy' in headers
        assert 'Referrer-Policy' in headers
        assert 'Permissions-Policy' in headers
        
        assert headers['X-Content-Type-Options'] == 'nosniff'
        assert headers['X-Frame-Options'] == 'DENY'
        assert headers['X-XSS-Protection'] == '1; mode=block'

class TestGlobalFunctions:
    """Test global rate limiter functions"""
    
    @patch('utils.rate_limiter.rate_limiter')
    def test_get_rate_limiter(self, mock_rate_limiter):
        """Test get_rate_limiter function"""
        from utils.rate_limiter import get_rate_limiter
        
        result = get_rate_limiter()
        assert result == mock_rate_limiter
    
    @patch('utils.rate_limiter.ddos_protection')
    def test_get_ddos_protection(self, mock_ddos_protection):
        """Test get_ddos_protection function"""
        from utils.rate_limiter import get_ddos_protection
        
        result = get_ddos_protection()
        assert result == mock_ddos_protection
    
    @patch('utils.rate_limiter.rate_limiter')
    def test_check_rate_limit(self, mock_rate_limiter):
        """Test check_rate_limit function"""
        mock_rate_limiter.is_allowed.return_value = (True, "Allowed", {})
        
        from utils.rate_limiter import check_rate_limit
        
        result = check_rate_limit("192.168.1.1", "agent1")
        
        assert result == (True, "Allowed", {})
        mock_rate_limiter.is_allowed.assert_called_once_with("192.168.1.1", "agent1", None)
    
    @patch('utils.rate_limiter.ddos_protection')
    def test_analyze_request_pattern(self, mock_ddos_protection):
        """Test analyze_request_pattern function"""
        mock_ddos_protection.analyze_request_pattern.return_value = (True, "Pattern analysis passed")
        
        from utils.rate_limiter import analyze_request_pattern
        
        result = analyze_request_pattern("192.168.1.1", "agent1", "/test")
        
        assert result == (True, "Pattern analysis passed")
        mock_ddos_protection.analyze_request_pattern.assert_called_once_with("192.168.1.1", "agent1", "/test")

class TestIntegration:
    """Test integration scenarios"""
    
    def test_rate_limiter_with_different_algorithms(self):
        """Test rate limiter with different algorithms"""
        # Test Token Bucket
        rule_token = RateLimitRule(algorithm=RateLimitAlgorithm.TOKEN_BUCKET)
        limiter_token = RateLimiter(rule_token)
        
        allowed, reason, details = limiter_token.is_allowed("192.168.1.1", "agent1")
        assert allowed is True
        
        # Test Sliding Window
        rule_sliding = RateLimitRule(algorithm=RateLimitAlgorithm.SLIDING_WINDOW)
        limiter_sliding = RateLimiter(rule_sliding)
        
        allowed, reason, details = limiter_sliding.is_allowed("192.168.1.1", "agent1")
        assert allowed is True
        
        # Test Leaky Bucket
        rule_leaky = RateLimitRule(algorithm=RateLimitAlgorithm.LEAKY_BUCKET)
        limiter_leaky = RateLimiter(rule_leaky)
        
        allowed, reason, details = limiter_leaky.is_allowed("192.168.1.1", "agent1")
        assert allowed is True
    
    def test_ddos_protection_with_rate_limiter(self):
        """Test DDoS protection integration with rate limiter"""
        rule = RateLimitRule()
        rate_limiter = RateLimiter(rule)
        ddos_protection = DDoSProtection(rate_limiter)
        
        # Normal request
        allowed, reason = ddos_protection.analyze_request_pattern("192.168.1.1", "agent1", "/test")
        assert allowed is True
        
        # Rate limit check
        allowed, reason, details = rate_limiter.is_allowed("192.168.1.1", "agent1")
        assert allowed is True

