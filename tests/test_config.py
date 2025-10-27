"""
Test suite for configuration system
"""
import pytest
import os
from unittest.mock import patch, Mock
from config import Config

class TestConfig:
    """Test configuration system"""
    
    def test_config_initialization(self):
        """Test config initialization"""
        config = Config()
        assert config is not None
        assert hasattr(config, 'LLM_MODEL')
        assert hasattr(config, 'LLM_BASE_URL')
        assert hasattr(config, 'PINECONE_API_KEY')
    
    @patch('config.get_secrets_manager')
    def test_config_with_secrets_manager(self, mock_get_secrets_manager):
        """Test config with secrets manager"""
        mock_secrets_manager = Mock()
        mock_secrets_manager.get_secret.return_value = "test_secret"
        mock_get_secrets_manager.return_value = mock_secrets_manager
        
        config = Config()
        
        # Test that secrets manager is used
        assert config.secrets_manager == mock_secrets_manager
    
    def test_validate_config(self):
        """Test config validation"""
        config = Config()
        
        # This should not raise an exception
        result = config.validate_config()
        assert result is True
    
    @patch.dict(os.environ, {'OLLAMA_BASE_URL': 'http://test:11434'})
    def test_config_with_environment_variables(self):
        """Test config with environment variables"""
        config = Config()
        assert config.LLM_BASE_URL == 'http://test:11434'
    
    def test_get_secret_fallback(self):
        """Test secret retrieval with fallback to environment"""
        config = Config()
        
        # Mock secrets manager to return None
        config.secrets_manager = Mock()
        config.secrets_manager.get_secret.return_value = None
        
        # Mock environment variable
        with patch.dict(os.environ, {'TEST_SECRET': 'env_value'}):
            result = config._get_secret('TEST_SECRET')
            assert result == 'env_value'
    
    def test_get_secret_from_manager(self):
        """Test secret retrieval from secrets manager"""
        config = Config()
        
        # Mock secrets manager to return a value
        config.secrets_manager = Mock()
        config.secrets_manager.get_secret.return_value = 'secret_value'
        
        result = config._get_secret('TEST_SECRET')
        assert result == 'secret_value'
        config.secrets_manager.get_secret.assert_called_once_with('TEST_SECRET')
