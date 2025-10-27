"""
Performance Monitoring System
Comprehensive performance tracking and optimization for the marketing agent system
"""
import time
import psutil
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json
import logging
from functools import wraps
import gc

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Performance metric data structure"""
    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    tags: Dict[str, str]

@dataclass
class SystemMetrics:
    """System performance metrics"""
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    network_io_bytes: int
    process_count: int
    load_average: List[float]

@dataclass
class ApplicationMetrics:
    """Application-specific metrics"""
    active_requests: int
    completed_requests: int
    error_requests: int
    average_response_time: float
    cache_hit_rate: float
    memory_usage_mb: float
    thread_count: int

class PerformanceMonitor:
    """Comprehensive performance monitoring system"""
    
    def __init__(self, collection_interval: int = 30):
        """
        Initialize performance monitor
        
        Args:
            collection_interval: Metrics collection interval in seconds
        """
        self.collection_interval = collection_interval
        self.metrics: List[PerformanceMetric] = []
        self.metrics_lock = threading.Lock()
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Performance thresholds
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'response_time': 5.0,
            'error_rate': 5.0
        }
        
        # Alert callbacks
        self.alert_callbacks: List[callable] = []
    
    def start_monitoring(self):
        """Start performance monitoring"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Collect system metrics
                system_metrics = self._collect_system_metrics()
                self._record_metrics(system_metrics)
                
                # Check for alerts
                self._check_alerts(system_metrics)
                
                # Clean up old metrics
                self._cleanup_old_metrics()
                
                time.sleep(self.collection_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.collection_interval)
    
    def _collect_system_metrics(self) -> SystemMetrics:
        """Collect system performance metrics"""
        try:
            # CPU and memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            # Load average (Unix only)
            try:
                load_avg = list(psutil.getloadavg())
            except AttributeError:
                load_avg = [0.0, 0.0, 0.0]
            
            return SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / (1024 * 1024),
                memory_available_mb=memory.available / (1024 * 1024),
                disk_usage_percent=disk.percent,
                network_io_bytes=network.bytes_sent + network.bytes_recv,
                process_count=len(psutil.pids()),
                load_average=load_avg
            )
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return SystemMetrics(0, 0, 0, 0, 0, 0, 0, [0, 0, 0])
    
    def _record_metrics(self, system_metrics: SystemMetrics):
        """Record metrics with thread safety"""
        with self.metrics_lock:
            current_time = datetime.now()
            
            # Record system metrics
            metrics_to_record = [
                ('cpu_percent', system_metrics.cpu_percent, '%'),
                ('memory_percent', system_metrics.memory_percent, '%'),
                ('memory_used_mb', system_metrics.memory_used_mb, 'MB'),
                ('disk_usage_percent', system_metrics.disk_usage_percent, '%'),
                ('process_count', system_metrics.process_count, 'count'),
                ('load_average_1m', system_metrics.load_average[0], 'load'),
                ('load_average_5m', system_metrics.load_average[1], 'load'),
                ('load_average_15m', system_metrics.load_average[2], 'load')
            ]
            
            for metric_name, value, unit in metrics_to_record:
                metric = PerformanceMetric(
                    timestamp=current_time,
                    metric_name=metric_name,
                    value=value,
                    unit=unit,
                    tags={'source': 'system'}
                )
                self.metrics.append(metric)
    
    def _check_alerts(self, system_metrics: SystemMetrics):
        """Check for performance alerts"""
        alerts = []
        
        if system_metrics.cpu_percent > self.thresholds['cpu_percent']:
            alerts.append(f"High CPU usage: {system_metrics.cpu_percent:.1f}%")
        
        if system_metrics.memory_percent > self.thresholds['memory_percent']:
            alerts.append(f"High memory usage: {system_metrics.memory_percent:.1f}%")
        
        if system_metrics.disk_usage_percent > 90:
            alerts.append(f"High disk usage: {system_metrics.disk_usage_percent:.1f}%")
        
        # Trigger alert callbacks
        for alert in alerts:
            for callback in self.alert_callbacks:
                try:
                    callback(alert, system_metrics)
                except Exception as e:
                    logger.error(f"Error in alert callback: {e}")
    
    def _cleanup_old_metrics(self):
        """Clean up old metrics to prevent memory leaks"""
        with self.metrics_lock:
            cutoff_time = datetime.now() - timedelta(hours=24)
            self.metrics = [m for m in self.metrics if m.timestamp > cutoff_time]
    
    def get_metrics_summary(self, hours: int = 1) -> Dict[str, Any]:
        """Get metrics summary for the last N hours"""
        with self.metrics_lock:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_metrics = [m for m in self.metrics if m.timestamp > cutoff_time]
        
        if not recent_metrics:
            return {}
        
        # Group metrics by name
        metric_groups = {}
        for metric in recent_metrics:
            if metric.metric_name not in metric_groups:
                metric_groups[metric.metric_name] = []
            metric_groups[metric.metric_name].append(metric.value)
        
        # Calculate statistics
        summary = {}
        for metric_name, values in metric_groups.items():
            summary[metric_name] = {
                'count': len(values),
                'min': min(values),
                'max': max(values),
                'avg': sum(values) / len(values),
                'latest': values[-1] if values else 0
            }
        
        return summary
    
    def add_alert_callback(self, callback: callable):
        """Add alert callback function"""
        self.alert_callbacks.append(callback)
    
    def set_threshold(self, metric: str, value: float):
        """Set performance threshold"""
        if metric in self.thresholds:
            self.thresholds[metric] = value
            logger.info(f"Threshold for {metric} set to {value}")
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        system_metrics = self._collect_system_metrics()
        return asdict(system_metrics)

def performance_timer(metric_name: str):
    """Decorator to time function execution"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                execution_time = time.time() - start_time
                # Record timing metric
                if hasattr(performance_monitor, 'metrics'):
                    with performance_monitor.metrics_lock:
                        metric = PerformanceMetric(
                            timestamp=datetime.now(),
                            metric_name=f"{metric_name}_execution_time",
                            value=execution_time,
                            unit='seconds',
                            tags={'function': func.__name__}
                        )
                        performance_monitor.metrics.append(metric)
        return wrapper
    return decorator

def memory_profiler(func):
    """Decorator to profile memory usage"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        memory_before = process.memory_info().rss / (1024 * 1024)  # MB
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            memory_after = process.memory_info().rss / (1024 * 1024)  # MB
            memory_delta = memory_after - memory_before
            
            # Record memory metric
            if hasattr(performance_monitor, 'metrics'):
                with performance_monitor.metrics_lock:
                    metric = PerformanceMetric(
                        timestamp=datetime.now(),
                        metric_name=f"{func.__name__}_memory_delta",
                        value=memory_delta,
                        unit='MB',
                        tags={'function': func.__name__}
                    )
                    performance_monitor.metrics.append(metric)
    return wrapper

class ApplicationPerformanceTracker:
    """Track application-specific performance metrics"""
    
    def __init__(self):
        self.request_times: List[float] = []
        self.error_count = 0
        self.success_count = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.lock = threading.Lock()
    
    def record_request(self, execution_time: float, success: bool = True):
        """Record request performance"""
        with self.lock:
            self.request_times.append(execution_time)
            if success:
                self.success_count += 1
            else:
                self.error_count += 1
    
    def record_cache_hit(self):
        """Record cache hit"""
        with self.lock:
            self.cache_hits += 1
    
    def record_cache_miss(self):
        """Record cache miss"""
        with self.lock:
            self.cache_misses += 1
    
    def get_stats(self) -> ApplicationMetrics:
        """Get application performance statistics"""
        with self.lock:
            total_requests = self.success_count + self.error_count
            error_rate = (self.error_count / total_requests * 100) if total_requests > 0 else 0
            avg_response_time = sum(self.request_times) / len(self.request_times) if self.request_times else 0
            cache_hit_rate = (self.cache_hits / (self.cache_hits + self.cache_misses) * 100) if (self.cache_hits + self.cache_misses) > 0 else 0
            
            return ApplicationMetrics(
                active_requests=0,  # This would need to be tracked separately
                completed_requests=total_requests,
                error_requests=self.error_count,
                average_response_time=avg_response_time,
                cache_hit_rate=cache_hit_rate,
                memory_usage_mb=psutil.Process().memory_info().rss / (1024 * 1024),
                thread_count=threading.active_count()
            )

# Global performance monitor instance
performance_monitor = PerformanceMonitor()
app_tracker = ApplicationPerformanceTracker()

def initialize_performance_monitoring():
    """Initialize performance monitoring system"""
    performance_monitor.start_monitoring()
    
    # Add default alert callback
    def default_alert_callback(alert: str, metrics: SystemMetrics):
        logger.warning(f"Performance Alert: {alert}")
        # In production, you might want to send alerts to monitoring services
    
    performance_monitor.add_alert_callback(default_alert_callback)
    logger.info("Performance monitoring initialized")

def cleanup_performance_monitoring():
    """Clean up performance monitoring"""
    performance_monitor.stop_monitoring()
    logger.info("Performance monitoring cleaned up")
