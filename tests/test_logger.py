"""
Comprehensive tests for the logging system
"""
import pytest
import json
import os
import tempfile
from datetime import datetime
from unittest.mock import patch, MagicMock

from utils.logger import (
    LoggerManager, SecurityLogger, PerformanceLogger, BusinessLogger, 
    AuditLogger, LogLevel, LogCategory, get_logger, log_performance
)

class TestLoggerManager:
    """Test LoggerManager functionality"""
    
    def test_logger_manager_initialization(self):
        """Test logger manager initialization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_level="INFO",
                log_dir=temp_dir
            )
            
            assert logger_manager.service_name == "test-service"
            assert logger_manager.log_level == 20  # INFO level
            assert os.path.exists(temp_dir)
    
    def test_logger_manager_with_invalid_level(self):
        """Test logger manager with invalid log level"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_level="INVALID",
                log_dir=temp_dir
            )
            
            # Should default to INFO level
            assert logger_manager.log_level == 20
    
    def test_get_logger(self):
        """Test getting logger instance"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            logger = logger_manager.get_logger("test_module")
            assert logger.name == "test-service.test_module"
    
    def test_logger_cleanup(self):
        """Test logger cleanup"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            # Should not raise any exceptions
            logger_manager.logger.info("Test message")

class TestSecurityLogger:
    """Test SecurityLogger functionality"""
    
    def test_security_logger_initialization(self):
        """Test security logger initialization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            security_logger = SecurityLogger(logger_manager.logger)
            assert security_logger.logger is not None
    
    def test_log_authentication_attempt(self):
        """Test logging authentication attempts"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            security_logger = SecurityLogger(logger_manager.logger)
            
            # Should not raise any exceptions
            security_logger.log_authentication_attempt(
                user_id="test_user",
                ip_address="192.168.1.1",
                success=True,
                user_agent="test_agent"
            )
    
    def test_log_suspicious_activity(self):
        """Test logging suspicious activities"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            security_logger = SecurityLogger(logger_manager.logger)
            
            # Should not raise any exceptions
            security_logger.log_suspicious_activity(
                activity_type="multiple_failed_logins",
                ip_address="192.168.1.1",
                user_id="test_user"
            )
    
    def test_log_input_validation_failure(self):
        """Test logging input validation failures"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            security_logger = SecurityLogger(logger_manager.logger)
            
            # Should not raise any exceptions
            security_logger.log_input_validation_failure(
                input_type="email",
                value="invalid_email",
                ip_address="192.168.1.1",
                user_id="test_user"
            )

class TestPerformanceLogger:
    """Test PerformanceLogger functionality"""
    
    def test_performance_logger_initialization(self):
        """Test performance logger initialization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            performance_logger = PerformanceLogger(logger_manager.logger)
            assert performance_logger.logger is not None
    
    def test_log_request_performance(self):
        """Test logging request performance"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            performance_logger = PerformanceLogger(logger_manager.logger)
            
            # Should not raise any exceptions
            performance_logger.log_request_performance(
                request_id="test_request",
                endpoint="/test",
                duration_ms=150.5,
                status_code=200,
                memory_usage_mb=256.7,
                cpu_usage_percent=15.3
            )
    
    def test_log_slow_query(self):
        """Test logging slow queries"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            performance_logger = PerformanceLogger(logger_manager.logger)
            
            # Should not raise any exceptions
            performance_logger.log_slow_query(
                query="SELECT * FROM large_table",
                duration_ms=5000.0,
                table_name="large_table"
            )
    
    def test_log_memory_usage(self):
        """Test logging memory usage"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            performance_logger = PerformanceLogger(logger_manager.logger)
            
            # Should not raise any exceptions
            performance_logger.log_memory_usage(
                component="test_component",
                memory_mb=512.0,
                threshold_mb=1024.0
            )

class TestBusinessLogger:
    """Test BusinessLogger functionality"""
    
    def test_business_logger_initialization(self):
        """Test business logger initialization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            business_logger = BusinessLogger(logger_manager.logger)
            assert business_logger.logger is not None
    
    def test_log_campaign_created(self):
        """Test logging campaign creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            business_logger = BusinessLogger(logger_manager.logger)
            
            # Should not raise any exceptions
            business_logger.log_campaign_created(
                campaign_id="test_campaign",
                hotel_name="Test Hotel",
                budget=1000.0,
                user_id="test_user"
            )
    
    def test_log_analysis_completed(self):
        """Test logging analysis completion"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            business_logger = BusinessLogger(logger_manager.logger)
            
            # Should not raise any exceptions
            business_logger.log_analysis_completed(
                request_id="test_request",
                hotel_name="Test Hotel",
                duration_ms=30000.0,
                user_id="test_user"
            )

class TestAuditLogger:
    """Test AuditLogger functionality"""
    
    def test_audit_logger_initialization(self):
        """Test audit logger initialization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            audit_logger = AuditLogger(logger_manager.logger)
            assert audit_logger.logger is not None
    
    def test_log_user_action(self):
        """Test logging user actions"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            audit_logger = AuditLogger(logger_manager.logger)
            
            # Should not raise any exceptions
            audit_logger.log_user_action(
                user_id="test_user",
                action="login",
                resource="user_account",
                ip_address="192.168.1.1",
                user_agent="test_agent"
            )
    
    def test_log_data_access(self):
        """Test logging data access"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            audit_logger = AuditLogger(logger_manager.logger)
            
            # Should not raise any exceptions
            audit_logger.log_data_access(
                user_id="test_user",
                data_type="hotel_data",
                operation="read",
                ip_address="192.168.1.1"
            )

class TestLogPerformanceDecorator:
    """Test log_performance decorator"""
    
    def test_log_performance_decorator(self):
        """Test log_performance decorator functionality"""
        
        @log_performance
        def test_function():
            return "test_result"
        
        # Should not raise any exceptions
        result = test_function()
        assert result == "test_result"
    
    def test_log_performance_decorator_with_exception(self):
        """Test log_performance decorator with exception"""
        
        @log_performance
        def test_function_with_error():
            raise ValueError("Test error")
        
        # Should raise the original exception
        with pytest.raises(ValueError, match="Test error"):
            test_function_with_error()

class TestLogLevels:
    """Test log level functionality"""
    
    def test_log_levels(self):
        """Test log level enumeration"""
        assert LogLevel.DEBUG.value == "DEBUG"
        assert LogLevel.INFO.value == "INFO"
        assert LogLevel.WARNING.value == "WARNING"
        assert LogLevel.ERROR.value == "ERROR"
        assert LogLevel.CRITICAL.value == "CRITICAL"
    
    def test_log_categories(self):
        """Test log category enumeration"""
        assert LogCategory.SYSTEM.value == "system"
        assert LogCategory.SECURITY.value == "security"
        assert LogCategory.PERFORMANCE.value == "performance"
        assert LogCategory.BUSINESS.value == "business"
        assert LogCategory.AUDIT.value == "audit"
        assert LogCategory.ERROR.value == "error"

class TestGlobalLoggerFunctions:
    """Test global logger functions"""
    
    def test_get_logger(self):
        """Test get_logger function"""
        logger = get_logger("test_module")
        assert logger is not None
        assert "test_module" in logger.name
    
    def test_log_functions(self):
        """Test global log functions"""
        # These should not raise any exceptions
        from utils.logger import log_info, log_warning, log_error, log_critical
        
        log_info("Test info message")
        log_warning("Test warning message")
        log_error("Test error message")
        log_critical("Test critical message")

class TestStructuredLogging:
    """Test structured logging functionality"""
    
    def test_structured_logging_format(self):
        """Test structured logging format"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger_manager = LoggerManager(
                service_name="test-service",
                log_dir=temp_dir
            )
            
            # Test that logs are written in JSON format
            logger = logger_manager.get_logger("test")
            logger.info("Test message", extra={
                'category': 'test',
                'metadata': {'test_key': 'test_value'}
            })
            
            # Check if log file exists and contains JSON
            log_files = [f for f in os.listdir(temp_dir) if f.endswith('.log')]
            assert len(log_files) > 0
            
            # Read the log file and verify JSON format
            with open(os.path.join(temp_dir, log_files[0]), 'r') as f:
                log_content = f.read()
                # Should contain JSON structure
                assert '"message"' in log_content
                assert '"category"' in log_content

