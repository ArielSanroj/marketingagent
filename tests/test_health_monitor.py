"""
Comprehensive tests for the health monitoring system
"""
import pytest
import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, Mock

from utils.health_monitor import (
    HealthStatus, ServiceStatus, HealthCheck, SystemMetrics,
    ApplicationMetrics, HealthMonitor, get_health_monitor,
    start_health_monitoring, stop_health_monitoring, get_health_status,
    get_metrics_history
)

class TestHealthStatus:
    """Test HealthStatus enumeration"""
    
    def test_health_status_values(self):
        """Test health status enumeration values"""
        assert HealthStatus.HEALTHY.value == "healthy"
        assert HealthStatus.WARNING.value == "warning"
        assert HealthStatus.CRITICAL.value == "critical"
        assert HealthStatus.UNKNOWN.value == "unknown"

class TestServiceStatus:
    """Test ServiceStatus enumeration"""
    
    def test_service_status_values(self):
        """Test service status enumeration values"""
        assert ServiceStatus.UP.value == "up"
        assert ServiceStatus.DOWN.value == "down"
        assert ServiceStatus.DEGRADED.value == "degraded"
        assert ServiceStatus.UNKNOWN.value == "unknown"

class TestHealthCheck:
    """Test HealthCheck dataclass"""
    
    def test_health_check_initialization(self):
        """Test health check initialization"""
        now = datetime.now()
        check = HealthCheck(
            service="test_service",
            status=HealthStatus.HEALTHY,
            message="Service is healthy",
            response_time_ms=150.5,
            timestamp=now
        )
        
        assert check.service == "test_service"
        assert check.status == HealthStatus.HEALTHY
        assert check.message == "Service is healthy"
        assert check.response_time_ms == 150.5
        assert check.timestamp == now
        assert check.details is None
    
    def test_health_check_with_details(self):
        """Test health check with details"""
        now = datetime.now()
        details = {"cpu_usage": 50.0, "memory_usage": 75.0}
        check = HealthCheck(
            service="test_service",
            status=HealthStatus.WARNING,
            message="Service is under stress",
            response_time_ms=500.0,
            timestamp=now,
            details=details
        )
        
        assert check.details == details

class TestSystemMetrics:
    """Test SystemMetrics dataclass"""
    
    def test_system_metrics_initialization(self):
        """Test system metrics initialization"""
        now = datetime.now()
        metrics = SystemMetrics(
            cpu_usage_percent=25.5,
            memory_usage_mb=512.0,
            memory_usage_percent=50.0,
            disk_usage_percent=75.0,
            network_io_bytes=1024000,
            process_count=150,
            load_average=[1.5, 1.2, 1.0],
            uptime_seconds=3600.0,
            timestamp=now
        )
        
        assert metrics.cpu_usage_percent == 25.5
        assert metrics.memory_usage_mb == 512.0
        assert metrics.memory_usage_percent == 50.0
        assert metrics.disk_usage_percent == 75.0
        assert metrics.network_io_bytes == 1024000
        assert metrics.process_count == 150
        assert metrics.load_average == [1.5, 1.2, 1.0]
        assert metrics.uptime_seconds == 3600.0
        assert metrics.timestamp == now

class TestApplicationMetrics:
    """Test ApplicationMetrics dataclass"""
    
    def test_application_metrics_initialization(self):
        """Test application metrics initialization"""
        now = datetime.now()
        metrics = ApplicationMetrics(
            active_requests=5,
            completed_requests=100,
            failed_requests=2,
            average_response_time_ms=250.5,
            requests_per_minute=25.0,
            error_rate_percent=2.0,
            memory_usage_mb=256.7,
            timestamp=now
        )
        
        assert metrics.active_requests == 5
        assert metrics.completed_requests == 100
        assert metrics.failed_requests == 2
        assert metrics.average_response_time_ms == 250.5
        assert metrics.requests_per_minute == 25.0
        assert metrics.error_rate_percent == 2.0
        assert metrics.memory_usage_mb == 256.7
        assert metrics.timestamp == now

@patch('utils.health_monitor.psutil')
class TestHealthMonitor:
    """Test HealthMonitor functionality"""
    
    def test_health_monitor_initialization(self, mock_psutil):
        """Test health monitor initialization"""
        monitor = HealthMonitor()
        
        assert monitor.health_checks == []
        assert monitor.system_metrics == []
        assert monitor.application_metrics == []
        assert monitor.monitoring_active is False
        assert monitor.monitoring_thread is None
        assert monitor.thresholds['cpu_usage_percent'] == 80.0
        assert monitor.thresholds['memory_usage_percent'] == 85.0
        assert monitor.thresholds['disk_usage_percent'] == 90.0
        assert monitor.thresholds['response_time_ms'] == 5000.0
        assert monitor.thresholds['error_rate_percent'] == 5.0
    
    def test_start_monitoring(self, mock_psutil):
        """Test starting health monitoring"""
        monitor = HealthMonitor()
        
        monitor.start_monitoring(interval_seconds=1)
        
        assert monitor.monitoring_active is True
        assert monitor.monitoring_thread is not None
        assert monitor.monitoring_thread.daemon is True
        
        # Stop monitoring to clean up
        monitor.stop_monitoring()
    
    def test_stop_monitoring(self, mock_psutil):
        """Test stopping health monitoring"""
        monitor = HealthMonitor()
        
        monitor.start_monitoring(interval_seconds=1)
        monitor.stop_monitoring()
        
        assert monitor.monitoring_active is False
    
    def test_collect_system_metrics_success(self, mock_psutil):
        """Test successful system metrics collection"""
        # Mock psutil functions
        mock_psutil.cpu_percent.return_value = 25.5
        mock_psutil.virtual_memory.return_value = Mock(used=1024*1024*512, percent=50.0)
        mock_psutil.disk_usage.return_value = Mock(used=1024*1024*1024*75, total=1024*1024*1024*100)
        mock_psutil.net_io_counters.return_value = Mock(bytes_sent=512000, bytes_recv=512000)
        mock_psutil.pids.return_value = list(range(150))
        mock_psutil.getloadavg.return_value = (1.5, 1.2, 1.0)
        mock_psutil.boot_time.return_value = time.time() - 3600
        
        monitor = HealthMonitor()
        metrics = monitor._collect_system_metrics()
        
        assert isinstance(metrics, SystemMetrics)
        assert metrics.cpu_usage_percent == 25.5
        assert metrics.memory_usage_mb == 512.0
        assert metrics.memory_usage_percent == 50.0
        assert metrics.disk_usage_percent == 75.0
        assert metrics.network_io_bytes == 1024000
        assert metrics.process_count == 150
        assert metrics.load_average == [1.5, 1.2, 1.0]
        assert metrics.uptime_seconds > 0
    
    def test_collect_system_metrics_error(self, mock_psutil):
        """Test system metrics collection with error"""
        mock_psutil.cpu_percent.side_effect = Exception("CPU error")
        
        monitor = HealthMonitor()
        metrics = monitor._collect_system_metrics()
        
        assert isinstance(metrics, SystemMetrics)
        assert metrics.cpu_usage_percent == 0.0
        assert metrics.memory_usage_mb == 0.0
        assert metrics.process_count == 0
    
    def test_collect_application_metrics(self, mock_psutil):
        """Test application metrics collection"""
        monitor = HealthMonitor()
        metrics = monitor._collect_application_metrics()
        
        assert isinstance(metrics, ApplicationMetrics)
        assert metrics.active_requests == 5
        assert metrics.completed_requests == 150
        assert metrics.failed_requests == 2
        assert metrics.average_response_time_ms == 250.5
        assert metrics.requests_per_minute == 25.0
        assert metrics.error_rate_percent == 1.3
        assert metrics.memory_usage_mb == 256.7
    
    @patch('utils.health_monitor.get_database_manager')
    def test_check_database_success(self, mock_get_db_manager, mock_psutil):
        """Test successful database health check"""
        mock_db_manager = MagicMock()
        mock_db_pool = MagicMock()
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        
        mock_db_manager.db_pool = mock_db_pool
        mock_db_pool.get_connection.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_get_db_manager.return_value = mock_db_manager
        
        monitor = HealthMonitor()
        check = monitor._check_database()
        
        assert isinstance(check, HealthCheck)
        assert check.service == "database"
        assert check.status == HealthStatus.HEALTHY
        assert "successful" in check.message
        assert check.response_time_ms > 0
    
    @patch('utils.health_monitor.get_database_manager')
    def test_check_database_failure(self, mock_get_db_manager, mock_psutil):
        """Test database health check failure"""
        mock_get_db_manager.side_effect = Exception("Database error")
        
        monitor = HealthMonitor()
        check = monitor._check_database()
        
        assert isinstance(check, HealthCheck)
        assert check.service == "database"
        assert check.status == HealthStatus.CRITICAL
        assert "error" in check.message.lower()
    
    @patch('utils.health_monitor.get_database_manager')
    def test_check_redis_success(self, mock_get_db_manager, mock_psutil):
        """Test successful Redis health check"""
        mock_db_manager = MagicMock()
        mock_redis_cache = MagicMock()
        mock_redis_client = MagicMock()
        
        mock_db_manager.redis_cache = mock_redis_cache
        mock_redis_cache.redis_client = mock_redis_client
        mock_redis_client.ping.return_value = True
        mock_redis_cache.get_stats.return_value = {"connected_clients": 5}
        mock_get_db_manager.return_value = mock_db_manager
        
        monitor = HealthMonitor()
        check = monitor._check_redis()
        
        assert isinstance(check, HealthCheck)
        assert check.service == "redis"
        assert check.status == HealthStatus.HEALTHY
        assert "successful" in check.message
        assert check.details == {"connected_clients": 5}
    
    @patch('utils.health_monitor.get_database_manager')
    def test_check_redis_not_configured(self, mock_get_db_manager, mock_psutil):
        """Test Redis health check when not configured"""
        mock_db_manager = MagicMock()
        mock_db_manager.redis_cache = None
        mock_get_db_manager.return_value = mock_db_manager
        
        monitor = HealthMonitor()
        check = monitor._check_redis()
        
        assert isinstance(check, HealthCheck)
        assert check.service == "redis"
        assert check.status == HealthStatus.WARNING
        assert "not configured" in check.message
    
    def test_check_external_apis(self, mock_psutil):
        """Test external API health checks"""
        monitor = HealthMonitor()
        checks = monitor._check_external_apis()
        
        assert isinstance(checks, list)
        assert len(checks) > 0
        
        # Check for Google Ads API
        google_ads_check = next((c for c in checks if c.service == "google_ads_api"), None)
        assert google_ads_check is not None
        assert isinstance(google_ads_check, HealthCheck)
    
    def test_check_alerts_system_metrics(self, mock_psutil):
        """Test alert checking for system metrics"""
        monitor = HealthMonitor()
        
        # Create high CPU usage metrics
        system_metrics = SystemMetrics(
            cpu_usage_percent=90.0,  # Above threshold
            memory_usage_mb=512.0,
            memory_usage_percent=50.0,
            disk_usage_percent=75.0,
            network_io_bytes=1024000,
            process_count=150,
            load_average=[1.5, 1.2, 1.0],
            uptime_seconds=3600.0,
            timestamp=datetime.now()
        )
        
        app_metrics = ApplicationMetrics(
            active_requests=5,
            completed_requests=100,
            failed_requests=2,
            average_response_time_ms=250.5,
            requests_per_minute=25.0,
            error_rate_percent=2.0,
            memory_usage_mb=256.7,
            timestamp=datetime.now()
        )
        
        # Should not raise any exceptions
        monitor._check_alerts(system_metrics, app_metrics, [])
    
    def test_check_alerts_application_metrics(self, mock_psutil):
        """Test alert checking for application metrics"""
        monitor = HealthMonitor()
        
        system_metrics = SystemMetrics(
            cpu_usage_percent=50.0,
            memory_usage_mb=512.0,
            memory_usage_percent=50.0,
            disk_usage_percent=75.0,
            network_io_bytes=1024000,
            process_count=150,
            load_average=[1.5, 1.2, 1.0],
            uptime_seconds=3600.0,
            timestamp=datetime.now()
        )
        
        # Create high error rate metrics
        app_metrics = ApplicationMetrics(
            active_requests=5,
            completed_requests=100,
            failed_requests=10,  # High failure count
            average_response_time_ms=6000.0,  # Above threshold
            requests_per_minute=25.0,
            error_rate_percent=10.0,  # Above threshold
            memory_usage_mb=256.7,
            timestamp=datetime.now()
        )
        
        # Should not raise any exceptions
        monitor._check_alerts(system_metrics, app_metrics, [])
    
    def test_check_alerts_health_checks(self, mock_psutil):
        """Test alert checking for health checks"""
        monitor = HealthMonitor()
        
        system_metrics = SystemMetrics(
            cpu_usage_percent=50.0,
            memory_usage_mb=512.0,
            memory_usage_percent=50.0,
            disk_usage_percent=75.0,
            network_io_bytes=1024000,
            process_count=150,
            load_average=[1.5, 1.2, 1.0],
            uptime_seconds=3600.0,
            timestamp=datetime.now()
        )
        
        app_metrics = ApplicationMetrics(
            active_requests=5,
            completed_requests=100,
            failed_requests=2,
            average_response_time_ms=250.5,
            requests_per_minute=25.0,
            error_rate_percent=2.0,
            memory_usage_mb=256.7,
            timestamp=datetime.now()
        )
        
        # Create critical health check
        health_checks = [
            HealthCheck(
                service="database",
                status=HealthStatus.CRITICAL,
                message="Database connection failed",
                response_time_ms=0.0,
                timestamp=datetime.now()
            )
        ]
        
        # Should not raise any exceptions
        monitor._check_alerts(system_metrics, app_metrics, health_checks)
    
    def test_get_health_status_healthy(self, mock_psutil):
        """Test getting health status when healthy"""
        monitor = HealthMonitor()
        
        # Add healthy metrics
        monitor.system_metrics = [
            SystemMetrics(
                cpu_usage_percent=50.0,
                memory_usage_mb=512.0,
                memory_usage_percent=50.0,
                disk_usage_percent=75.0,
                network_io_bytes=1024000,
                process_count=150,
                load_average=[1.5, 1.2, 1.0],
                uptime_seconds=3600.0,
                timestamp=datetime.now()
            )
        ]
        
        monitor.application_metrics = [
            ApplicationMetrics(
                active_requests=5,
                completed_requests=100,
                failed_requests=2,
                average_response_time_ms=250.5,
                requests_per_minute=25.0,
                error_rate_percent=2.0,
                memory_usage_mb=256.7,
                timestamp=datetime.now()
            )
        ]
        
        monitor.health_checks = [
            HealthCheck(
                service="database",
                status=HealthStatus.HEALTHY,
                message="Database is healthy",
                response_time_ms=150.0,
                timestamp=datetime.now()
            )
        ]
        
        status = monitor.get_health_status()
        
        assert status['status'] == 'healthy'
        assert 'timestamp' in status
        assert 'system_metrics' in status
        assert 'application_metrics' in status
        assert 'health_checks' in status
        assert 'critical_issues' in status
        assert 'warnings' in status
        assert 'monitoring_active' in status
    
    def test_get_health_status_warning(self, mock_psutil):
        """Test getting health status when warning"""
        monitor = HealthMonitor()
        
        # Add warning metrics (high CPU usage)
        monitor.system_metrics = [
            SystemMetrics(
                cpu_usage_percent=90.0,  # Above threshold
                memory_usage_mb=512.0,
                memory_usage_percent=50.0,
                disk_usage_percent=75.0,
                network_io_bytes=1024000,
                process_count=150,
                load_average=[1.5, 1.2, 1.0],
                uptime_seconds=3600.0,
                timestamp=datetime.now()
            )
        ]
        
        monitor.application_metrics = [
            ApplicationMetrics(
                active_requests=5,
                completed_requests=100,
                failed_requests=2,
                average_response_time_ms=250.5,
                requests_per_minute=25.0,
                error_rate_percent=2.0,
                memory_usage_mb=256.7,
                timestamp=datetime.now()
            )
        ]
        
        status = monitor.get_health_status()
        
        assert status['status'] == 'warning'
        assert len(status['warnings']) > 0
    
    def test_get_health_status_critical(self, mock_psutil):
        """Test getting health status when critical"""
        monitor = HealthMonitor()
        
        # Add critical health check
        monitor.health_checks = [
            HealthCheck(
                service="database",
                status=HealthStatus.CRITICAL,
                message="Database connection failed",
                response_time_ms=0.0,
                timestamp=datetime.now()
            )
        ]
        
        status = monitor.get_health_status()
        
        assert status['status'] == 'critical'
        assert len(status['critical_issues']) > 0
    
    def test_get_metrics_history(self, mock_psutil):
        """Test getting metrics history"""
        monitor = HealthMonitor()
        
        # Add some historical metrics
        now = datetime.now()
        monitor.system_metrics = [
            SystemMetrics(
                cpu_usage_percent=50.0,
                memory_usage_mb=512.0,
                memory_usage_percent=50.0,
                disk_usage_percent=75.0,
                network_io_bytes=1024000,
                process_count=150,
                load_average=[1.5, 1.2, 1.0],
                uptime_seconds=3600.0,
                timestamp=now - timedelta(minutes=30)
            ),
            SystemMetrics(
                cpu_usage_percent=60.0,
                memory_usage_mb=600.0,
                memory_usage_percent=60.0,
                disk_usage_percent=80.0,
                network_io_bytes=1200000,
                process_count=160,
                load_average=[1.8, 1.5, 1.2],
                uptime_seconds=3660.0,
                timestamp=now
            )
        ]
        
        monitor.application_metrics = [
            ApplicationMetrics(
                active_requests=5,
                completed_requests=100,
                failed_requests=2,
                average_response_time_ms=250.5,
                requests_per_minute=25.0,
                error_rate_percent=2.0,
                memory_usage_mb=256.7,
                timestamp=now - timedelta(minutes=30)
            ),
            ApplicationMetrics(
                active_requests=8,
                completed_requests=120,
                failed_requests=3,
                average_response_time_ms=300.0,
                requests_per_minute=30.0,
                error_rate_percent=2.5,
                memory_usage_mb=300.0,
                timestamp=now
            )
        ]
        
        history = monitor.get_metrics_history(hours=1)
        
        assert 'system_metrics' in history
        assert 'application_metrics' in history
        assert 'health_checks' in history
        assert 'time_range_hours' in history
        assert 'timestamp' in history
        assert len(history['system_metrics']) == 2
        assert len(history['application_metrics']) == 2

class TestGlobalFunctions:
    """Test global health monitor functions"""
    
    @patch('utils.health_monitor.health_monitor')
    def test_get_health_monitor(self, mock_health_monitor):
        """Test get_health_monitor function"""
        result = get_health_monitor()
        assert result == mock_health_monitor
    
    @patch('utils.health_monitor.health_monitor')
    def test_start_health_monitoring(self, mock_health_monitor):
        """Test start_health_monitoring function"""
        start_health_monitoring(interval_seconds=30)
        mock_health_monitor.start_monitoring.assert_called_once_with(30)
    
    @patch('utils.health_monitor.health_monitor')
    def test_stop_health_monitoring(self, mock_health_monitor):
        """Test stop_health_monitoring function"""
        stop_health_monitoring()
        mock_health_monitor.stop_monitoring.assert_called_once()
    
    @patch('utils.health_monitor.health_monitor')
    def test_get_health_status(self, mock_health_monitor):
        """Test get_health_status function"""
        mock_health_monitor.get_health_status.return_value = {"status": "healthy"}
        
        result = get_health_status()
        assert result == {"status": "healthy"}
        mock_health_monitor.get_health_status.assert_called_once()
    
    @patch('utils.health_monitor.health_monitor')
    def test_get_metrics_history(self, mock_health_monitor):
        """Test get_metrics_history function"""
        mock_health_monitor.get_metrics_history.return_value = {"metrics": "data"}
        
        result = get_metrics_history(hours=2)
        assert result == {"metrics": "data"}
        mock_health_monitor.get_metrics_history.assert_called_once_with(2)

class TestIntegration:
    """Test integration scenarios"""
    
    @patch('utils.health_monitor.psutil')
    def test_full_monitoring_cycle(self, mock_psutil):
        """Test full monitoring cycle"""
        # Mock psutil functions
        mock_psutil.cpu_percent.return_value = 50.0
        mock_psutil.virtual_memory.return_value = Mock(used=1024*1024*512, percent=50.0)
        mock_psutil.disk_usage.return_value = Mock(used=1024*1024*1024*75, total=1024*1024*1024*100)
        mock_psutil.net_io_counters.return_value = Mock(bytes_sent=512000, bytes_recv=512000)
        mock_psutil.pids.return_value = list(range(150))
        mock_psutil.getloadavg.return_value = (1.5, 1.2, 1.0)
        mock_psutil.boot_time.return_value = time.time() - 3600
        
        monitor = HealthMonitor()
        
        # Test system metrics collection
        system_metrics = monitor._collect_system_metrics()
        assert isinstance(system_metrics, SystemMetrics)
        
        # Test application metrics collection
        app_metrics = monitor._collect_application_metrics()
        assert isinstance(app_metrics, ApplicationMetrics)
        
        # Test health checks
        health_checks = monitor._perform_health_checks()
        assert isinstance(health_checks, list)
        
        # Test alert checking
        monitor._check_alerts(system_metrics, app_metrics, health_checks)
        
        # Test getting health status
        status = monitor.get_health_status()
        assert 'status' in status
        assert 'timestamp' in status
    
    def test_monitoring_thread_lifecycle(self):
        """Test monitoring thread lifecycle"""
        monitor = HealthMonitor()
        
        # Start monitoring
        monitor.start_monitoring(interval_seconds=1)
        assert monitor.monitoring_active is True
        assert monitor.monitoring_thread is not None
        
        # Stop monitoring
        monitor.stop_monitoring()
        assert monitor.monitoring_active is False

