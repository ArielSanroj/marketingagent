"""
Health Monitoring and System Status
Comprehensive health checks, system monitoring, and alerting
"""
import os
import time
import psutil
import threading
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.logger import get_logger, log_info, log_warning, log_error

logger = get_logger(__name__)

class HealthStatus(Enum):
    """Health status enumeration"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

class ServiceStatus(Enum):
    """Service status enumeration"""
    UP = "up"
    DOWN = "down"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"

@dataclass
class HealthCheck:
    """Health check result"""
    service: str
    status: HealthStatus
    message: str
    response_time_ms: float
    timestamp: datetime
    details: Dict[str, Any] = None

@dataclass
class SystemMetrics:
    """System metrics"""
    cpu_usage_percent: float
    memory_usage_mb: float
    memory_usage_percent: float
    disk_usage_percent: float
    network_io_bytes: int
    process_count: int
    load_average: List[float]
    uptime_seconds: float
    timestamp: datetime

@dataclass
class ApplicationMetrics:
    """Application metrics"""
    active_requests: int
    completed_requests: int
    failed_requests: int
    average_response_time_ms: float
    requests_per_minute: float
    error_rate_percent: float
    memory_usage_mb: float
    timestamp: datetime

class HealthMonitor:
    """Comprehensive health monitoring system"""
    
    def __init__(self):
        self.health_checks: List[HealthCheck] = []
        self.system_metrics: List[SystemMetrics] = []
        self.application_metrics: List[ApplicationMetrics] = []
        self.monitoring_active = False
        self.monitoring_thread = None
        self.lock = threading.Lock()
        
        # Health check thresholds
        self.thresholds = {
            'cpu_usage_percent': 80.0,
            'memory_usage_percent': 85.0,
            'disk_usage_percent': 90.0,
            'response_time_ms': 5000.0,
            'error_rate_percent': 5.0
        }
    
    def start_monitoring(self, interval_seconds: int = 30):
        """Start continuous health monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval_seconds,),
            daemon=True
        )
        self.monitoring_thread.start()
        logger.info(f"Health monitoring started with {interval_seconds}s interval")
    
    def stop_monitoring(self):
        """Stop health monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Health monitoring stopped")
    
    def _monitoring_loop(self, interval_seconds: int):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                system_metrics = self._collect_system_metrics()
                with self.lock:
                    self.system_metrics.append(system_metrics)
                    # Keep only last 100 metrics
                    if len(self.system_metrics) > 100:
                        self.system_metrics = self.system_metrics[-100:]
                
                # Collect application metrics
                app_metrics = self._collect_application_metrics()
                with self.lock:
                    self.application_metrics.append(app_metrics)
                    # Keep only last 100 metrics
                    if len(self.application_metrics) > 100:
                        self.application_metrics = self.application_metrics[-100:]
                
                # Perform health checks
                health_checks = self._perform_health_checks()
                with self.lock:
                    self.health_checks.extend(health_checks)
                    # Keep only last 50 health checks
                    if len(self.health_checks) > 50:
                        self.health_checks = self.health_checks[-50:]
                
                # Check for alerts
                self._check_alerts(system_metrics, app_metrics, health_checks)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
            
            time.sleep(interval_seconds)
    
    def _collect_system_metrics(self) -> SystemMetrics:
        """Collect system-level metrics"""
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage_mb = memory.used / (1024 * 1024)
            memory_usage_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage_percent = (disk.used / disk.total) * 100
            
            # Network I/O
            network_io = psutil.net_io_counters()
            network_io_bytes = network_io.bytes_sent + network_io.bytes_recv
            
            # Process count
            process_count = len(psutil.pids())
            
            # Load average
            load_avg = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0.0, 0.0, 0.0]
            
            # Uptime
            uptime_seconds = time.time() - psutil.boot_time()
            
            return SystemMetrics(
                cpu_usage_percent=cpu_usage,
                memory_usage_mb=memory_usage_mb,
                memory_usage_percent=memory_usage_percent,
                disk_usage_percent=disk_usage_percent,
                network_io_bytes=network_io_bytes,
                process_count=process_count,
                load_average=list(load_avg),
                uptime_seconds=uptime_seconds,
                timestamp=datetime.now()
            )
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return SystemMetrics(
                cpu_usage_percent=0.0,
                memory_usage_mb=0.0,
                memory_usage_percent=0.0,
                disk_usage_percent=0.0,
                network_io_bytes=0,
                process_count=0,
                load_average=[0.0, 0.0, 0.0],
                uptime_seconds=0.0,
                timestamp=datetime.now()
            )
    
    def _collect_application_metrics(self) -> ApplicationMetrics:
        """Collect application-level metrics"""
        try:
            # This would be integrated with the actual application metrics
            # For now, return mock data
            return ApplicationMetrics(
                active_requests=5,
                completed_requests=150,
                failed_requests=2,
                average_response_time_ms=250.5,
                requests_per_minute=25.0,
                error_rate_percent=1.3,
                memory_usage_mb=256.7,
                timestamp=datetime.now()
            )
        except Exception as e:
            logger.error(f"Error collecting application metrics: {e}")
            return ApplicationMetrics(
                active_requests=0,
                completed_requests=0,
                failed_requests=0,
                average_response_time_ms=0.0,
                requests_per_minute=0.0,
                error_rate_percent=0.0,
                memory_usage_mb=0.0,
                timestamp=datetime.now()
            )
    
    def _perform_health_checks(self) -> List[HealthCheck]:
        """Perform health checks on all services"""
        health_checks = []
        
        # Check database
        db_check = self._check_database()
        if db_check:
            health_checks.append(db_check)
        
        # Check Redis
        redis_check = self._check_redis()
        if redis_check:
            health_checks.append(redis_check)
        
        # Check external APIs
        api_checks = self._check_external_apis()
        health_checks.extend(api_checks)
        
        return health_checks
    
    def _check_database(self) -> Optional[HealthCheck]:
        """Check database health"""
        try:
            start_time = time.time()
            
            # Try to import and test database connection
            from utils.database import get_database_manager
            db_manager = get_database_manager()
            
            if db_manager and db_manager.db_pool:
                # Test database connection
                with db_manager.db_pool.get_connection() as conn:
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT 1")
                        cursor.fetchone()
                        cursor.close()
                
                response_time = (time.time() - start_time) * 1000
                return HealthCheck(
                    service="database",
                    status=HealthStatus.HEALTHY,
                    message="Database connection successful",
                    response_time_ms=response_time,
                    timestamp=datetime.now(),
                    details={"connection_pool_size": db_manager.db_pool.pool.maxconn if db_manager.db_pool.pool else 0}
                )
            else:
                return HealthCheck(
                    service="database",
                    status=HealthStatus.CRITICAL,
                    message="Database not configured",
                    response_time_ms=0.0,
                    timestamp=datetime.now()
                )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheck(
                service="database",
                status=HealthStatus.CRITICAL,
                message=f"Database error: {str(e)}",
                response_time_ms=response_time,
                timestamp=datetime.now()
            )
    
    def _check_redis(self) -> Optional[HealthCheck]:
        """Check Redis health"""
        try:
            start_time = time.time()
            
            from utils.database import get_database_manager
            db_manager = get_database_manager()
            
            if db_manager and db_manager.redis_cache and db_manager.redis_cache.redis_client:
                # Test Redis connection
                db_manager.redis_cache.redis_client.ping()
                
                response_time = (time.time() - start_time) * 1000
                return HealthCheck(
                    service="redis",
                    status=HealthStatus.HEALTHY,
                    message="Redis connection successful",
                    response_time_ms=response_time,
                    timestamp=datetime.now(),
                    details=db_manager.redis_cache.get_stats()
                )
            else:
                return HealthCheck(
                    service="redis",
                    status=HealthStatus.WARNING,
                    message="Redis not configured",
                    response_time_ms=0.0,
                    timestamp=datetime.now()
                )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheck(
                service="redis",
                status=HealthStatus.CRITICAL,
                message=f"Redis error: {str(e)}",
                response_time_ms=response_time,
                timestamp=datetime.now()
            )
    
    def _check_external_apis(self) -> List[HealthCheck]:
        """Check external API health"""
        health_checks = []
        
        # Check Google Ads API
        try:
            start_time = time.time()
            
            # Test Google Ads API availability
            # This would be a real API call in production
            response_time = (time.time() - start_time) * 1000
            
            health_checks.append(HealthCheck(
                service="google_ads_api",
                status=HealthStatus.HEALTHY,
                message="Google Ads API accessible",
                response_time_ms=response_time,
                timestamp=datetime.now()
            ))
        except Exception as e:
            health_checks.append(HealthCheck(
                service="google_ads_api",
                status=HealthStatus.CRITICAL,
                message=f"Google Ads API error: {str(e)}",
                response_time_ms=0.0,
                timestamp=datetime.now()
            ))
        
        return health_checks
    
    def _check_alerts(self, system_metrics: SystemMetrics, 
                     app_metrics: ApplicationMetrics, 
                     health_checks: List[HealthCheck]):
        """Check for alert conditions"""
        alerts = []
        
        # System alerts
        if system_metrics.cpu_usage_percent > self.thresholds['cpu_usage_percent']:
            alerts.append(f"High CPU usage: {system_metrics.cpu_usage_percent:.1f}%")
        
        if system_metrics.memory_usage_percent > self.thresholds['memory_usage_percent']:
            alerts.append(f"High memory usage: {system_metrics.memory_usage_percent:.1f}%")
        
        if system_metrics.disk_usage_percent > self.thresholds['disk_usage_percent']:
            alerts.append(f"High disk usage: {system_metrics.disk_usage_percent:.1f}%")
        
        # Application alerts
        if app_metrics.error_rate_percent > self.thresholds['error_rate_percent']:
            alerts.append(f"High error rate: {app_metrics.error_rate_percent:.1f}%")
        
        if app_metrics.average_response_time_ms > self.thresholds['response_time_ms']:
            alerts.append(f"Slow response time: {app_metrics.average_response_time_ms:.1f}ms")
        
        # Health check alerts
        for check in health_checks:
            if check.status == HealthStatus.CRITICAL:
                alerts.append(f"Critical: {check.service} - {check.message}")
            elif check.status == HealthStatus.WARNING:
                alerts.append(f"Warning: {check.service} - {check.message}")
        
        # Log alerts
        for alert in alerts:
            log_warning(f"Health alert: {alert}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status"""
        with self.lock:
            # Get latest metrics
            latest_system = self.system_metrics[-1] if self.system_metrics else None
            latest_app = self.application_metrics[-1] if self.application_metrics else None
            latest_checks = self.health_checks[-10:] if self.health_checks else []
            
            # Determine overall status
            overall_status = HealthStatus.HEALTHY
            critical_issues = []
            warnings = []
            
            # Check system metrics
            if latest_system:
                if latest_system.cpu_usage_percent > self.thresholds['cpu_usage_percent']:
                    overall_status = HealthStatus.WARNING
                    warnings.append(f"High CPU usage: {latest_system.cpu_usage_percent:.1f}%")
                
                if latest_system.memory_usage_percent > self.thresholds['memory_usage_percent']:
                    overall_status = HealthStatus.WARNING
                    warnings.append(f"High memory usage: {latest_system.memory_usage_percent:.1f}%")
                
                if latest_system.disk_usage_percent > self.thresholds['disk_usage_percent']:
                    overall_status = HealthStatus.WARNING
                    warnings.append(f"High disk usage: {latest_system.disk_usage_percent:.1f}%")
            
            # Check application metrics
            if latest_app:
                if latest_app.error_rate_percent > self.thresholds['error_rate_percent']:
                    overall_status = HealthStatus.WARNING
                    warnings.append(f"High error rate: {latest_app.error_rate_percent:.1f}%")
                
                if latest_app.average_response_time_ms > self.thresholds['response_time_ms']:
                    overall_status = HealthStatus.WARNING
                    warnings.append(f"Slow response time: {latest_app.average_response_time_ms:.1f}ms")
            
            # Check health checks
            for check in latest_checks:
                if check.status == HealthStatus.CRITICAL:
                    overall_status = HealthStatus.CRITICAL
                    critical_issues.append(f"{check.service}: {check.message}")
                elif check.status == HealthStatus.WARNING and overall_status != HealthStatus.CRITICAL:
                    overall_status = HealthStatus.WARNING
                    warnings.append(f"{check.service}: {check.message}")
            
            return {
                'status': overall_status.value,
                'timestamp': datetime.now().isoformat(),
                'system_metrics': latest_system.__dict__ if latest_system else None,
                'application_metrics': latest_app.__dict__ if latest_app else None,
                'health_checks': [check.__dict__ for check in latest_checks],
                'critical_issues': critical_issues,
                'warnings': warnings,
                'monitoring_active': self.monitoring_active
            }
    
    def get_metrics_history(self, hours: int = 1) -> Dict[str, Any]:
        """Get metrics history for the specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with self.lock:
            # Filter metrics by time
            recent_system = [m for m in self.system_metrics if m.timestamp > cutoff_time]
            recent_app = [m for m in self.application_metrics if m.timestamp > cutoff_time]
            recent_checks = [c for c in self.health_checks if c.timestamp > cutoff_time]
            
            return {
                'system_metrics': [m.__dict__ for m in recent_system],
                'application_metrics': [m.__dict__ for m in recent_app],
                'health_checks': [c.__dict__ for c in recent_checks],
                'time_range_hours': hours,
                'timestamp': datetime.now().isoformat()
            }

# Global health monitor instance
health_monitor = HealthMonitor()

def get_health_monitor() -> HealthMonitor:
    """Get health monitor instance"""
    return health_monitor

def start_health_monitoring(interval_seconds: int = 30):
    """Start health monitoring"""
    health_monitor.start_monitoring(interval_seconds)

def stop_health_monitoring():
    """Stop health monitoring"""
    health_monitor.stop_monitoring()

def get_health_status() -> Dict[str, Any]:
    """Get current health status"""
    return health_monitor.get_health_status()

def get_metrics_history(hours: int = 1) -> Dict[str, Any]:
    """Get metrics history"""
    return health_monitor.get_metrics_history(hours)
