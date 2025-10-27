"""
Configuration settings for the Hotel Sales Multi-Agent System
"""
import os
from dotenv import load_dotenv
from utils.secrets_manager import get_secrets_manager

load_dotenv()

class Config:
    """Configuration class for the hotel sales system"""
    
    def __init__(self):
        """Initialize configuration with secrets management"""
        self.secrets_manager = get_secrets_manager(os.getenv('SECRETS_MANAGER_TYPE', 'local'))
        self._load_secrets()
    
    def _load_secrets(self):
        """Load secrets from appropriate source"""
        # LLM Configuration
        self.LLM_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.1:8b')
        self.LLM_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        
        # Pinecone Configuration
        self.PINECONE_API_KEY = self._get_secret('PINECONE_API_KEY')
        self.PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')
        self.PINECONE_INDEX_NAME = 'hotel-sales-memory'
        
        # Google Ads Configuration
        self.GOOGLE_ADS_DEVELOPER_TOKEN = self._get_secret('GOOGLE_ADS_DEVELOPER_TOKEN')
        self.GOOGLE_ADS_CLIENT_ID = self._get_secret('GOOGLE_ADS_CLIENT_ID')
        self.GOOGLE_ADS_CLIENT_SECRET = self._get_secret('GOOGLE_ADS_CLIENT_SECRET')
        self.GOOGLE_ADS_REFRESH_TOKEN = self._get_secret('GOOGLE_ADS_REFRESH_TOKEN')
        self.GOOGLE_ADS_LOGIN_CUSTOMER_ID = self._get_secret('GOOGLE_ADS_LOGIN_CUSTOMER_ID')
    
    def _get_secret(self, key: str) -> str:
        """Get secret from secrets manager or environment"""
        # Try secrets manager first
        secret = self.secrets_manager.get_secret(key)
        if secret:
            return secret
        
        # Fallback to environment variable
        return os.getenv(key)
    
        # Memory Configuration
        self.EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
        self.EMBEDDING_DIMENSION = 384
        self.MAX_MEMORY_RETRIEVAL = 10
        
        # Agent Configuration
        self.MAX_ITERATIONS = 3
        self.MAX_EXECUTION_TIME = 300
        self.VERBOSE = True
        
        # Campaign Configuration
        self.DEFAULT_BUDGET = 1000
        self.DEFAULT_TARGET_ROAS = 400
        self.DEFAULT_CPC_BID = 2.50
        
        # File Paths
        self.OUTPUT_DIR = "outputs"
        self.LOGS_DIR = "logs"
    
    def validate_config(self):
        """Validate configuration and provide helpful warnings for optional services"""
        warnings = []
        errors = []
        
        # Check for LLM configuration
        if not os.getenv('OPENAI_API_KEY') and not os.getenv('OLLAMA_BASE_URL'):
            warnings.append("No LLM configured. Set either OPENAI_API_KEY or OLLAMA_BASE_URL")
        
        # Check for Pinecone (optional but recommended)
        if not self.PINECONE_API_KEY:
            warnings.append("PINECONE_API_KEY not set. Memory will use local file storage only")
        
        # Check for Google Ads (optional)
        google_ads_vars = [
            'GOOGLE_ADS_DEVELOPER_TOKEN',
            'GOOGLE_ADS_CLIENT_ID', 
            'GOOGLE_ADS_CLIENT_SECRET',
            'GOOGLE_ADS_REFRESH_TOKEN',
            'GOOGLE_ADS_LOGIN_CUSTOMER_ID'
        ]
        missing_google_ads = []
        for var in google_ads_vars:
            if not getattr(self, var, None):
                missing_google_ads.append(var)
        
        if missing_google_ads:
            warnings.append(f"Google Ads API not fully configured. Missing: {', '.join(missing_google_ads)}. Will use simulator.")
        
        # Print warnings
        if warnings:
            print("⚠️  Configuration Warnings:")
            for warning in warnings:
                print(f"   - {warning}")
            print()
        
        # Print errors and fail if critical
        if errors:
            print("❌ Configuration Errors:")
            for error in errors:
                print(f"   - {error}")
            raise ValueError("Critical configuration errors found")
        
        return True

# Global config instance
config = Config()