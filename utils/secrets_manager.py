"""
Secrets Management System
Handles secure storage and retrieval of sensitive configuration data
"""
import os
import json
import base64
from typing import Dict, Any, Optional, Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

logger = logging.getLogger(__name__)

class SecretsManager:
    """Secure secrets management for production environments"""
    
    def __init__(self, master_key: Optional[str] = None):
        """
        Initialize secrets manager
        
        Args:
            master_key: Master encryption key. If None, will use environment variable or generate new one
        """
        self.master_key = master_key or os.getenv('MASTER_SECRET_KEY')
        self._fernet = None
        self._initialize_encryption()
    
    def _initialize_encryption(self):
        """Initialize encryption using master key"""
        try:
            if not self.master_key:
                # Generate a new master key if none provided
                self.master_key = Fernet.generate_key().decode()
                logger.warning("No master key provided. Generated new key. Store this securely!")
                print(f"🔑 NEW MASTER KEY: {self.master_key}")
                print("⚠️  Store this key securely in your environment variables!")
            
            # Derive encryption key from master key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'marketing_agent_salt',  # In production, use random salt
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
            self._fernet = Fernet(key)
            
        except Exception as e:
            logger.error(f"Failed to initialize encryption: {e}")
            raise ValueError(f"Secrets manager initialization failed: {e}")
    
    def encrypt_secret(self, value: str) -> str:
        """Encrypt a secret value"""
        try:
            if not self._fernet:
                raise ValueError("Encryption not initialized")
            
            encrypted_value = self._fernet.encrypt(value.encode())
            return base64.urlsafe_b64encode(encrypted_value).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt secret: {e}")
            raise ValueError(f"Encryption failed: {e}")
    
    def decrypt_secret(self, encrypted_value: str) -> str:
        """Decrypt a secret value"""
        try:
            if not self._fernet:
                raise ValueError("Encryption not initialized")
            
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_value.encode())
            decrypted_value = self._fernet.decrypt(encrypted_bytes)
            return decrypted_value.decode()
        except Exception as e:
            logger.error(f"Failed to decrypt secret: {e}")
            raise ValueError(f"Decryption failed: {e}")
    
    def store_secret(self, key: str, value: str, encrypted: bool = True) -> bool:
        """Store a secret securely"""
        try:
            secrets_file = os.getenv('SECRETS_FILE', 'secrets.encrypted')
            
            # Load existing secrets
            secrets = self._load_secrets(secrets_file)
            
            # Encrypt value if requested
            if encrypted:
                secrets[key] = self.encrypt_secret(value)
            else:
                secrets[key] = value
            
            # Save secrets
            self._save_secrets(secrets, secrets_file)
            logger.info(f"Secret '{key}' stored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store secret '{key}': {e}")
            return False
    
    def get_secret(self, key: str, encrypted: bool = True) -> Optional[str]:
        """Retrieve a secret"""
        try:
            secrets_file = os.getenv('SECRETS_FILE', 'secrets.encrypted')
            secrets = self._load_secrets(secrets_file)
            
            if key not in secrets:
                return None
            
            value = secrets[key]
            
            # Decrypt if encrypted
            if encrypted:
                return self.decrypt_secret(value)
            else:
                return value
                
        except Exception as e:
            logger.error(f"Failed to retrieve secret '{key}': {e}")
            return None
    
    def delete_secret(self, key: str) -> bool:
        """Delete a secret"""
        try:
            secrets_file = os.getenv('SECRETS_FILE', 'secrets.encrypted')
            secrets = self._load_secrets(secrets_file)
            
            if key in secrets:
                del secrets[key]
                self._save_secrets(secrets, secrets_file)
                logger.info(f"Secret '{key}' deleted successfully")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete secret '{key}': {e}")
            return False
    
    def list_secrets(self) -> list:
        """List all stored secret keys"""
        try:
            secrets_file = os.getenv('SECRETS_FILE', 'secrets.encrypted')
            secrets = self._load_secrets(secrets_file)
            return list(secrets.keys())
        except Exception as e:
            logger.error(f"Failed to list secrets: {e}")
            return []
    
    def _load_secrets(self, filepath: str) -> Dict[str, str]:
        """Load secrets from file"""
        if not os.path.exists(filepath):
            return {}
        
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load secrets from {filepath}: {e}")
            return {}
    
    def _save_secrets(self, secrets: Dict[str, str], filepath: str):
        """Save secrets to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(secrets, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save secrets to {filepath}: {e}")
            raise

class EnvironmentSecretsManager:
    """Environment-based secrets manager for cloud deployments"""
    
    def __init__(self):
        self.prefix = os.getenv('SECRETS_PREFIX', 'MARKETING_AGENT_')
    
    def get_secret(self, key: str) -> Optional[str]:
        """Get secret from environment variable"""
        env_key = f"{self.prefix}{key.upper()}"
        return os.getenv(env_key)
    
    def set_secret(self, key: str, value: str) -> bool:
        """Set secret in environment (for current process only)"""
        try:
            env_key = f"{self.prefix}{key.upper()}"
            os.environ[env_key] = value
            return True
        except Exception as e:
            logger.error(f"Failed to set environment secret '{key}': {e}")
            return False

class CloudSecretsManager:
    """Cloud-based secrets manager (AWS Secrets Manager, Azure Key Vault, etc.)"""
    
    def __init__(self, provider: str = 'aws'):
        self.provider = provider
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize cloud secrets client"""
        try:
            if self.provider == 'aws':
                import boto3
                self._client = boto3.client('secretsmanager')
            elif self.provider == 'azure':
                from azure.keyvault.secrets import SecretClient
                from azure.identity import DefaultAzureCredential
                credential = DefaultAzureCredential()
                vault_url = os.getenv('AZURE_KEY_VAULT_URL')
                if not vault_url:
                    raise ValueError("AZURE_KEY_VAULT_URL environment variable required")
                self._client = SecretClient(vault_url=vault_url, credential=credential)
            else:
                raise ValueError(f"Unsupported cloud provider: {self.provider}")
                
        except Exception as e:
            logger.error(f"Failed to initialize cloud secrets client: {e}")
            raise
    
    def get_secret(self, key: str) -> Optional[str]:
        """Get secret from cloud provider"""
        try:
            if self.provider == 'aws':
                response = self._client.get_secret_value(SecretId=key)
                return response['SecretString']
            elif self.provider == 'azure':
                secret = self._client.get_secret(key)
                return secret.value
        except Exception as e:
            logger.error(f"Failed to get cloud secret '{key}': {e}")
            return None
    
    def set_secret(self, key: str, value: str) -> bool:
        """Set secret in cloud provider"""
        try:
            if self.provider == 'aws':
                self._client.create_secret(
                    Name=key,
                    SecretString=value
                )
            elif self.provider == 'azure':
                self._client.set_secret(key, value)
            return True
        except Exception as e:
            logger.error(f"Failed to set cloud secret '{key}': {e}")
            return False

def get_secrets_manager(manager_type: str = 'local') -> Union[SecretsManager, EnvironmentSecretsManager, CloudSecretsManager]:
    """
    Factory function to get appropriate secrets manager
    
    Args:
        manager_type: Type of secrets manager ('local', 'env', 'cloud')
    
    Returns:
        Appropriate secrets manager instance
    """
    if manager_type == 'local':
        return SecretsManager()
    elif manager_type == 'env':
        return EnvironmentSecretsManager()
    elif manager_type == 'cloud':
        provider = os.getenv('CLOUD_SECRETS_PROVIDER', 'aws')
        return CloudSecretsManager(provider)
    else:
        raise ValueError(f"Unknown secrets manager type: {manager_type}")

# Global secrets manager instance
secrets_manager = get_secrets_manager(os.getenv('SECRETS_MANAGER_TYPE', 'local'))
