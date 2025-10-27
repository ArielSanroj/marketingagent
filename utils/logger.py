"""
Comprehensive Logging System
Structured JSON logging with performance tracking, security monitoring, and audit trails
"""
import json
import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import traceback
import threading
from functools import wraps

class LogLevel(Enum):
    """Log level enumeration"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogCategory(Enum):
    """Log category enumeration"""
    SYSTEM = "system"
    SECURITY = "security"
    PERFORMANCE = "performance"
    BUSINESS = "business"
    AUDIT = "audit"
    ERROR = "error"

@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: str
    level: str
    category: str
    message: str
    service: str
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    duration_ms: Optional[float] = None
    memory_usage_mb: Optional[float] = None
    cpu_usage_percent: Optional[float] = None
    error_code: Optional[str] = None
    stack_trace: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging"""
    
    def __init__(self, service_name: str = "marketing-agent"):
        super().__init__()
        self.service_name = service_name
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON"""
        try:
            # Extract custom fields from record
            log_entry = LogEntry(
                timestamp=datetime.utcnow().isoformat() + "Z",
                level=record.levelname,
                category=getattr(record, 'category', LogCategory.SYSTEM.value),
                message=record.getMessage(),
                service=self.service_name,
                request_id=getattr(record, 'request_id', None),
                user_id=getattr(record, 'user_id', None),
                session_id=getattr(record, 'session_id', None),
                ip_address=getattr(record, 'ip_address', None),
                user_agent=getattr(record, 'user_agent', None),
                duration_ms=getattr(record, 'duration_ms', None),
                memory_usage_mb=getattr(record, 'memory_usage_mb', None),
                cpu_usage_percent=getattr(record, 'cpu_usage_percent', None),
                error_code=getattr(record, 'error_code', None),
                stack_trace=getattr(record, 'stack_trace', None),
                metadata=getattr(record, 'metadata', None)
            )
            
            return json.dumps(asdict(log_entry), ensure_ascii=False)
        except Exception as e:
            # Fallback to simple format if JSON serialization fails
            return f"{record.levelname}: {record.getMessage()}"

class SecurityLogger:
    """Specialized logger for security events"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_authentication_attempt(self, user_id: str, ip_address: str, success: bool, 
                                 user_agent: str = None, metadata: Dict[str, Any] = None):
        """Log authentication attempts"""
        self.logger.warning(
            f"Authentication attempt: user={user_id}, ip={ip_address}, success={success}",
            extra={
                'category': LogCategory.SECURITY.value,
                'user_id': user_id,
                'ip_address': ip_address,
                'user_agent': user_agent,
                'metadata': {
                    'event_type': 'authentication_attempt',
                    'success': success,
                    **(metadata or {})
                }
            }
        )
    
    def log_suspicious_activity(self, activity_type: str, ip_address: str, 
                              user_id: str = None, metadata: Dict[str, Any] = None):
        """Log suspicious activities"""
        self.logger.error(
            f"Suspicious activity detected: {activity_type}",
            extra={
                'category': LogCategory.SECURITY.value,
                'user_id': user_id,
                'ip_address': ip_address,
                'metadata': {
                    'event_type': 'suspicious_activity',
                    'activity_type': activity_type,
                    **(metadata or {})
                }
            }
        )
    
    def log_input_validation_failure(self, input_type: str, value: str, 
                                   ip_address: str, user_id: str = None):
        """Log input validation failures"""
        self.logger.warning(
            f"Input validation failed: {input_type}",
            extra={
                'category': LogCategory.SECURITY.value,
                'user_id': user_id,
                'ip_address': ip_address,
                'metadata': {
                    'event_type': 'input_validation_failure',
                    'input_type': input_type,
                    'value_length': len(str(value)),
                    'sanitized_value': str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                }
            }
        )

class PerformanceLogger:
    """Specialized logger for performance events"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_request_performance(self, request_id: str, endpoint: str, 
                              duration_ms: float, status_code: int, 
                              memory_usage_mb: float = None, cpu_usage_percent: float = None):
        """Log request performance metrics"""
        self.logger.info(
            f"Request completed: {endpoint}",
            extra={
                'category': LogCategory.PERFORMANCE.value,
                'request_id': request_id,
                'duration_ms': duration_ms,
                'memory_usage_mb': memory_usage_mb,
                'cpu_usage_percent': cpu_usage_percent,
                'metadata': {
                    'event_type': 'request_performance',
                    'endpoint': endpoint,
                    'status_code': status_code,
                    'duration_ms': duration_ms
                }
            }
        )
    
    def log_slow_query(self, query: str, duration_ms: float, 
                      table_name: str = None, metadata: Dict[str, Any] = None):
        """Log slow database queries"""
        self.logger.warning(
            f"Slow query detected: {duration_ms}ms",
            extra={
                'category': LogCategory.PERFORMANCE.value,
                'duration_ms': duration_ms,
                'metadata': {
                    'event_type': 'slow_query',
                    'query': query[:200] + "..." if len(query) > 200 else query,
                    'table_name': table_name,
                    'duration_ms': duration_ms,
                    **(metadata or {})
                }
            }
        )
    
    def log_memory_usage(self, component: str, memory_mb: float, 
                        threshold_mb: float = None, metadata: Dict[str, Any] = None):
        """Log memory usage events"""
        level = logging.WARNING if threshold_mb and memory_mb > threshold_mb else logging.INFO
        self.logger.log(
            level,
            f"Memory usage: {component}",
            extra={
                'category': LogCategory.PERFORMANCE.value,
                'memory_usage_mb': memory_mb,
                'metadata': {
                    'event_type': 'memory_usage',
                    'component': component,
                    'memory_mb': memory_mb,
                    'threshold_mb': threshold_mb,
                    **(metadata or {})
                }
            }
        )

class BusinessLogger:
    """Specialized logger for business events"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_campaign_created(self, campaign_id: str, hotel_name: str, 
                           budget: float, user_id: str = None, metadata: Dict[str, Any] = None):
        """Log campaign creation events"""
        self.logger.info(
            f"Campaign created: {campaign_id}",
            extra={
                'category': LogCategory.BUSINESS.value,
                'user_id': user_id,
                'metadata': {
                    'event_type': 'campaign_created',
                    'campaign_id': campaign_id,
                    'hotel_name': hotel_name,
                    'budget': budget,
                    **(metadata or {})
                }
            }
        )
    
    def log_analysis_completed(self, request_id: str, hotel_name: str, 
                             duration_ms: float, user_id: str = None, metadata: Dict[str, Any] = None):
        """Log analysis completion events"""
        self.logger.info(
            f"Analysis completed: {request_id}",
            extra={
                'category': LogCategory.BUSINESS.value,
                'request_id': request_id,
                'user_id': user_id,
                'duration_ms': duration_ms,
                'metadata': {
                    'event_type': 'analysis_completed',
                    'hotel_name': hotel_name,
                    'duration_ms': duration_ms,
                    **(metadata or {})
                }
            }
        )

class AuditLogger:
    """Specialized logger for audit events"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_user_action(self, user_id: str, action: str, resource: str, 
                       ip_address: str, user_agent: str = None, metadata: Dict[str, Any] = None):
        """Log user actions for audit trail"""
        self.logger.info(
            f"User action: {action}",
            extra={
                'category': LogCategory.AUDIT.value,
                'user_id': user_id,
                'ip_address': ip_address,
                'user_agent': user_agent,
                'metadata': {
                    'event_type': 'user_action',
                    'action': action,
                    'resource': resource,
                    **(metadata or {})
                }
            }
        )
    
    def log_data_access(self, user_id: str, data_type: str, operation: str, 
                       ip_address: str, metadata: Dict[str, Any] = None):
        """Log data access events"""
        self.logger.info(
            f"Data access: {operation}",
            extra={
                'category': LogCategory.AUDIT.value,
                'user_id': user_id,
                'ip_address': ip_address,
                'metadata': {
                    'event_type': 'data_access',
                    'data_type': data_type,
                    'operation': operation,
                    **(metadata or {})
                }
            }
        )

class LoggerManager:
    """Centralized logger management"""
    
    def __init__(self, service_name: str = "marketing-agent", 
                 log_level: str = "INFO", log_dir: str = "logs"):
        self.service_name = service_name
        self.log_dir = log_dir
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure root logger
        self._setup_loggers()
        
        # Create specialized loggers
        self.security = SecurityLogger(self.logger)
        self.performance = PerformanceLogger(self.logger)
        self.business = BusinessLogger(self.logger)
        self.audit = AuditLogger(self.logger)
    
    def _setup_loggers(self):
        """Setup all loggers with proper configuration"""
        # Main application logger
        self.logger = logging.getLogger(self.service_name)
        self.logger.setLevel(self.log_level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler for development
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        console_formatter = StructuredFormatter(self.service_name)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler for all logs
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.log_dir, f"{self.service_name}.log"),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(self.log_level)
        file_formatter = StructuredFormatter(self.service_name)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Error log handler
        error_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.log_dir, f"{self.service_name}_errors.log"),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = StructuredFormatter(self.service_name)
        error_handler.setFormatter(error_formatter)
        self.logger.addHandler(error_handler)
        
        # Security log handler
        security_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.log_dir, f"{self.service_name}_security.log"),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10
        )
        security_handler.setLevel(logging.WARNING)
        security_formatter = StructuredFormatter(self.service_name)
        security_handler.setFormatter(security_formatter)
        self.logger.addHandler(security_handler)
        
        # Performance log handler
        performance_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.log_dir, f"{self.service_name}_performance.log"),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        performance_handler.setLevel(logging.INFO)
        performance_formatter = StructuredFormatter(self.service_name)
        performance_handler.setFormatter(performance_formatter)
        self.logger.addHandler(performance_handler)
    
    def get_logger(self, name: str = None) -> logging.Logger:
        """Get logger instance"""
        if name:
            return logging.getLogger(f"{self.service_name}.{name}")
        return self.logger

def log_performance(func):
    """Decorator to log function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        function_name = f"{func.__module__}.{func.__name__}"
        
        try:
            result = func(*args, **kwargs)
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            # Log performance
            if hasattr(logger_manager, 'performance'):
                logger_manager.performance.log_request_performance(
                    request_id=getattr(args[0], 'request_id', None) if args else None,
                    endpoint=function_name,
                    duration_ms=duration_ms,
                    status_code=200
                )
            
            return result
        except Exception as e:
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            # Log error
            logger_manager.logger.error(
                f"Function error: {function_name}",
                extra={
                    'category': LogCategory.ERROR.value,
                    'error_code': type(e).__name__,
                    'stack_trace': traceback.format_exc(),
                    'duration_ms': duration_ms,
                    'metadata': {
                        'event_type': 'function_error',
                        'function_name': function_name,
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                }
            )
            raise
    return wrapper

def log_security_event(event_type: str, **kwargs):
    """Log security events"""
    logger_manager.security.logger.warning(
        f"Security event: {event_type}",
        extra={
            'category': LogCategory.SECURITY.value,
            'metadata': {
                'event_type': event_type,
                **kwargs
            }
        }
    )

# Global logger manager instance
logger_manager = LoggerManager(
    service_name=os.getenv('SERVICE_NAME', 'marketing-agent'),
    log_level=os.getenv('LOG_LEVEL', 'INFO'),
    log_dir=os.getenv('LOG_DIR', 'logs')
)

# Convenience functions
def get_logger(name: str = None) -> logging.Logger:
    """Get logger instance"""
    return logger_manager.get_logger(name)

def log_info(message: str, **kwargs):
    """Log info message"""
    logger_manager.logger.info(message, extra=kwargs)

def log_warning(message: str, **kwargs):
    """Log warning message"""
    logger_manager.logger.warning(message, extra=kwargs)

def log_error(message: str, **kwargs):
    """Log error message"""
    logger_manager.logger.error(message, extra=kwargs)

def log_critical(message: str, **kwargs):
    """Log critical message"""
    logger_manager.logger.critical(message, extra=kwargs)
