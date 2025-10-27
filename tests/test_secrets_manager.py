"""
Test suite for secrets management system
"""
import pytest
import os
import tempfile
from utils.secrets_manager import (
    SecretsManager, EnvironmentSecretsManager, CloudSecretsManager,
    get_secrets_manager
)

class TestSecretsManager:
    """Test local secrets manager"""
    
    def test_encryption_decryption(self):
        """Test encryption and decryption"""
        manager = SecretsManager()
        test_secret = "test_secret_value"
        
        encrypted = manager.encrypt_secret(test_secret)
        assert encrypted != test_secret
        assert len(encrypted) > 0
        
        decrypted = manager.decrypt_secret(encrypted)
        assert decrypted == test_secret
    
    def test_store_and_retrieve_secret(self):
        """Test storing and retrieving secrets"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            secrets_file = f.name
        
        try:
            manager = SecretsManager()
            manager._save_secrets = lambda secrets, filepath: None  # Mock save
            
            # Test storing secret
            result = manager.store_secret("test_key", "test_value")
            assert result
            
            # Test retrieving secret
            secret = manager.get_secret("test_key")
            assert secret == "test_value"
            
        finally:
            if os.path.exists(secrets_file):
                os.unlink(secrets_file)
    
    def test_delete_secret(self):
        """Test deleting secrets"""
        manager = SecretsManager()
        manager._save_secrets = lambda secrets, filepath: None  # Mock save
        
        # Store a secret
        manager.store_secret("test_key", "test_value")
        
        # Delete the secret
        result = manager.delete_secret("test_key")
        assert result
        
        # Verify secret is gone
        secret = manager.get_secret("test_key")
        assert secret is None

class TestEnvironmentSecretsManager:
    """Test environment-based secrets manager"""
    
    def test_get_secret_from_env(self):
        """Test getting secret from environment"""
        manager = EnvironmentSecretsManager()
        
        # Set environment variable
        os.environ["MARKETING_AGENT_TEST_SECRET"] = "test_value"
        
        try:
            secret = manager.get_secret("test_secret")
            assert secret == "test_value"
        finally:
            # Clean up
            if "MARKETING_AGENT_TEST_SECRET" in os.environ:
                del os.environ["MARKETING_AGENT_TEST_SECRET"]
    
    def test_set_secret_in_env(self):
        """Test setting secret in environment"""
        manager = EnvironmentSecretsManager()
        
        result = manager.set_secret("test_key", "test_value")
        assert result
        
        # Verify it was set
        assert os.environ.get("MARKETING_AGENT_TEST_KEY") == "test_value"
        
        # Clean up
        if "MARKETING_AGENT_TEST_KEY" in os.environ:
            del os.environ["MARKETING_AGENT_TEST_KEY"]

class TestSecretsManagerFactory:
    """Test secrets manager factory function"""
    
    def test_get_local_manager(self):
        """Test getting local secrets manager"""
        manager = get_secrets_manager("local")
        assert isinstance(manager, SecretsManager)
    
    def test_get_env_manager(self):
        """Test getting environment secrets manager"""
        manager = get_secrets_manager("env")
        assert isinstance(manager, EnvironmentSecretsManager)
    
    def test_get_cloud_manager(self):
        """Test getting cloud secrets manager"""
        # This will fail without proper cloud credentials, but we can test the factory
        with pytest.raises(Exception):
            get_secrets_manager("cloud")
    
    def test_invalid_manager_type(self):
        """Test invalid manager type"""
        with pytest.raises(ValueError):
            get_secrets_manager("invalid_type")
