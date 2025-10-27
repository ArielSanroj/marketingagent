"""
Rate Limiting and DDoS Protection System
Advanced rate limiting with multiple algorithms, IP-based protection, and adaptive throttling
"""
import time
import threading
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import json
from collections import defaultdict, deque
import logging

from utils.logger import get_logger, log_security_event

logger = get_logger(__name__)

class RateLimitAlgorithm(Enum):
    """Rate limiting algorithms"""
    TOKEN_BUCKET = "token_bucket"
    SLIDING_WINDOW = "sliding_window"
    FIXED_WINDOW = "fixed_window"
    LEAKY_BUCKET = "leaky_bucket"

class ThreatLevel(Enum):
    """Threat level classification"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class RateLimitRule:
    """Rate limiting rule configuration"""
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    requests_per_day: int = 10000
    burst_limit: int = 10
    algorithm: RateLimitAlgorithm = RateLimitAlgorithm.SLIDING_WINDOW
    block_duration_seconds: int = 300  # 5 minutes
    whitelist: List[str] = None
    blacklist: List[str] = None

@dataclass
class ClientInfo:
    """Client information for rate limiting"""
    ip_address: str
    user_agent: str
    first_seen: datetime
    last_request: datetime
    request_count: int = 0
    blocked_until: Optional[datetime] = None
    threat_level: ThreatLevel = ThreatLevel.LOW
    violations: int = 0

class TokenBucket:
    """Token bucket algorithm implementation"""
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens from bucket"""
        with self.lock:
            now = time.time()
            # Refill tokens based on time passed
            time_passed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + time_passed * self.refill_rate)
            self.last_refill = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

class SlidingWindow:
    """Sliding window algorithm implementation"""
    
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size  # seconds
        self.max_requests = max_requests
        self.requests = deque()
        self.lock = threading.Lock()
    
    def is_allowed(self) -> bool:
        """Check if request is allowed within window"""
        with self.lock:
            now = time.time()
            # Remove old requests outside window
            while self.requests and self.requests[0] <= now - self.window_size:
                self.requests.popleft()
            
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            return False

class LeakyBucket:
    """Leaky bucket algorithm implementation"""
    
    def __init__(self, capacity: int, leak_rate: float):
        self.capacity = capacity
        self.tokens = 0
        self.leak_rate = leak_rate
        self.last_leak = time.time()
        self.lock = threading.Lock()
    
    def add_request(self) -> bool:
        """Add request to bucket"""
        with self.lock:
            now = time.time()
            # Leak tokens based on time passed
            time_passed = now - self.last_leak
            self.tokens = max(0, self.tokens - time_passed * self.leak_rate)
            self.last_leak = now
            
            if self.tokens < self.capacity:
                self.tokens += 1
                return True
            return False

class RateLimiter:
    """Advanced rate limiter with multiple algorithms"""
    
    def __init__(self, default_rule: RateLimitRule = None):
        self.default_rule = default_rule or RateLimitRule()
        self.clients: Dict[str, ClientInfo] = {}
        self.rate_limiters: Dict[str, Any] = {}
        self.blocked_ips: Dict[str, datetime] = {}
        self.lock = threading.Lock()
        
        # Cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_expired, daemon=True)
        self.cleanup_thread.start()
    
    def _get_client_key(self, ip_address: str, user_agent: str = None) -> str:
        """Generate unique client key"""
        key_data = f"{ip_address}:{user_agent or 'unknown'}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_rate_limiter(self, client_key: str, rule: RateLimitRule) -> Any:
        """Get or create rate limiter for client"""
        if client_key not in self.rate_limiters:
            if rule.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
                self.rate_limiters[client_key] = TokenBucket(
                    capacity=rule.burst_limit,
                    refill_rate=rule.requests_per_minute / 60.0
                )
            elif rule.algorithm == RateLimitAlgorithm.SLIDING_WINDOW:
                self.rate_limiters[client_key] = SlidingWindow(
                    window_size=60,  # 1 minute window
                    max_requests=rule.requests_per_minute
                )
            elif rule.algorithm == RateLimitAlgorithm.LEAKY_BUCKET:
                self.rate_limiters[client_key] = LeakyBucket(
                    capacity=rule.burst_limit,
                    leak_rate=rule.requests_per_minute / 60.0
                )
        
        return self.rate_limiters[client_key]
    
    def _update_client_info(self, ip_address: str, user_agent: str, client_key: str):
        """Update client information"""
        now = datetime.now()
        
        if client_key not in self.clients:
            self.clients[client_key] = ClientInfo(
                ip_address=ip_address,
                user_agent=user_agent,
                first_seen=now,
                last_request=now
            )
        else:
            self.clients[client_key].last_request = now
        
        self.clients[client_key].request_count += 1
    
    def _assess_threat_level(self, client_key: str) -> ThreatLevel:
        """Assess threat level based on client behavior"""
        if client_key not in self.clients:
            return ThreatLevel.LOW
        
        client = self.clients[client_key]
        now = datetime.now()
        
        # Calculate requests per minute
        time_diff = (now - client.first_seen).total_seconds()
        if time_diff > 0:
            requests_per_minute = (client.request_count * 60) / time_diff
        else:
            requests_per_minute = 0
        
        # Assess threat level
        if requests_per_minute > 1000 or client.violations > 10:
            return ThreatLevel.CRITICAL
        elif requests_per_minute > 500 or client.violations > 5:
            return ThreatLevel.HIGH
        elif requests_per_minute > 200 or client.violations > 2:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def is_allowed(self, ip_address: str, user_agent: str = None, 
                  rule: RateLimitRule = None) -> Tuple[bool, str, Dict[str, Any]]:
        """Check if request is allowed"""
        rule = rule or self.default_rule
        client_key = self._get_client_key(ip_address, user_agent)
        
        # Check if IP is blocked
        if ip_address in self.blocked_ips:
            if datetime.now() < self.blocked_ips[ip_address]:
                return False, "IP blocked", {"blocked_until": self.blocked_ips[ip_address].isoformat()}
            else:
                # Unblock expired IP
                del self.blocked_ips[ip_address]
        
        # Check whitelist
        if rule.whitelist and ip_address in rule.whitelist:
            return True, "Whitelisted", {}
        
        # Check blacklist
        if rule.blacklist and ip_address in rule.blacklist:
            self._block_ip(ip_address, "Blacklisted")
            return False, "Blacklisted", {}
        
        # Update client info
        self._update_client_info(ip_address, user_agent, client_key)
        
        # Get rate limiter
        rate_limiter = self._get_rate_limiter(client_key, rule)
        
        # Check rate limit
        if rule.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
            allowed = rate_limiter.consume()
        elif rule.algorithm == RateLimitAlgorithm.SLIDING_WINDOW:
            allowed = rate_limiter.is_allowed()
        elif rule.algorithm == RateLimitAlgorithm.LEAKY_BUCKET:
            allowed = rate_limiter.add_request()
        else:
            allowed = True
        
        if not allowed:
            # Increment violation count
            if client_key in self.clients:
                self.clients[client_key].violations += 1
            
            # Assess threat level
            threat_level = self._assess_threat_level(client_key)
            self.clients[client_key].threat_level = threat_level
            
            # Block IP if threat level is high
            if threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
                self._block_ip(ip_address, f"High threat level: {threat_level.value}")
                log_security_event('rate_limit_exceeded', 
                                 ip_address=ip_address,
                                 threat_level=threat_level.value,
                                 violations=self.clients[client_key].violations)
            
            return False, "Rate limit exceeded", {
                "threat_level": threat_level.value,
                "violations": self.clients[client_key].violations
            }
        
        return True, "Allowed", {}
    
    def _block_ip(self, ip_address: str, reason: str):
        """Block IP address"""
        block_until = datetime.now() + timedelta(seconds=self.default_rule.block_duration_seconds)
        self.blocked_ips[ip_address] = block_until
        
        log_security_event('ip_blocked', 
                         ip_address=ip_address,
                         reason=reason,
                         blocked_until=block_until.isoformat())
    
    def _cleanup_expired(self):
        """Clean up expired data"""
        while True:
            try:
                time.sleep(300)  # Cleanup every 5 minutes
                
                with self.lock:
                    now = datetime.now()
                    
                    # Remove expired blocked IPs
                    expired_ips = [ip for ip, block_time in self.blocked_ips.items() 
                                 if now > block_time]
                    for ip in expired_ips:
                        del self.blocked_ips[ip]
                    
                    # Remove old client data (older than 24 hours)
                    old_clients = [key for key, client in self.clients.items() 
                                 if (now - client.last_request).total_seconds() > 86400]
                    for key in old_clients:
                        del self.clients[key]
                        if key in self.rate_limiters:
                            del self.rate_limiters[key]
                
                logger.debug(f"Rate limiter cleanup completed. Active clients: {len(self.clients)}")
            except Exception as e:
                logger.error(f"Rate limiter cleanup error: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiter statistics"""
        with self.lock:
            now = datetime.now()
            active_clients = len(self.clients)
            blocked_ips = len(self.blocked_ips)
            
            # Calculate threat level distribution
            threat_levels = defaultdict(int)
            for client in self.clients.values():
                threat_levels[client.threat_level.value] += 1
            
            return {
                'active_clients': active_clients,
                'blocked_ips': blocked_ips,
                'threat_level_distribution': dict(threat_levels),
                'total_requests': sum(client.request_count for client in self.clients.values()),
                'average_requests_per_client': sum(client.request_count for client in self.clients.values()) / max(active_clients, 1)
            }

class DDoSProtection:
    """DDoS protection system"""
    
    def __init__(self, rate_limiter: RateLimiter):
        self.rate_limiter = rate_limiter
        self.suspicious_patterns = defaultdict(int)
        self.attack_detection_threshold = 100  # requests per minute
        self.lock = threading.Lock()
    
    def analyze_request_pattern(self, ip_address: str, user_agent: str, 
                              endpoint: str) -> Tuple[bool, str]:
        """Analyze request pattern for DDoS indicators"""
        pattern_key = f"{ip_address}:{endpoint}"
        
        with self.lock:
            self.suspicious_patterns[pattern_key] += 1
            
            # Check for suspicious patterns
            if self.suspicious_patterns[pattern_key] > self.attack_detection_threshold:
                # Potential DDoS attack detected
                log_security_event('ddos_attack_detected', 
                                 ip_address=ip_address,
                                 endpoint=endpoint,
                                 request_count=self.suspicious_patterns[pattern_key])
                
                return False, "DDoS attack detected"
            
            return True, "Pattern analysis passed"
    
    def get_attack_stats(self) -> Dict[str, Any]:
        """Get DDoS attack statistics"""
        with self.lock:
            return {
                'suspicious_patterns': len(self.suspicious_patterns),
                'total_suspicious_requests': sum(self.suspicious_patterns.values()),
                'top_attackers': sorted(self.suspicious_patterns.items(), 
                                      key=lambda x: x[1], reverse=True)[:10]
            }

class SecurityHeaders:
    """Security headers middleware"""
    
    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """Get security headers for responses"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
        }

# Global rate limiter instance
rate_limiter = RateLimiter()
ddos_protection = DDoSProtection(rate_limiter)

def get_rate_limiter() -> RateLimiter:
    """Get rate limiter instance"""
    return rate_limiter

def get_ddos_protection() -> DDoSProtection:
    """Get DDoS protection instance"""
    return ddos_protection

def check_rate_limit(ip_address: str, user_agent: str = None, 
                    rule: RateLimitRule = None) -> Tuple[bool, str, Dict[str, Any]]:
    """Check rate limit for request"""
    return rate_limiter.is_allowed(ip_address, user_agent, rule)

def analyze_request_pattern(ip_address: str, user_agent: str, endpoint: str) -> Tuple[bool, str]:
    """Analyze request pattern for DDoS protection"""
    return ddos_protection.analyze_request_pattern(ip_address, user_agent, endpoint)
