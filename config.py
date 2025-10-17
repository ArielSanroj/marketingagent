"""
Configuration settings for the Hotel Sales Multi-Agent System
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the hotel sales system"""
    
    # LLM Configuration
    LLM_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.1:8b')
    LLM_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    
    # Pinecone Configuration
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')
    PINECONE_INDEX_NAME = 'hotel-sales-memory'
    
    # Google Ads Configuration
    GOOGLE_ADS_DEVELOPER_TOKEN = os.getenv('GOOGLE_ADS_DEVELOPER_TOKEN')
    GOOGLE_ADS_CLIENT_ID = os.getenv('GOOGLE_ADS_CLIENT_ID')
    GOOGLE_ADS_CLIENT_SECRET = os.getenv('GOOGLE_ADS_CLIENT_SECRET')
    GOOGLE_ADS_REFRESH_TOKEN = os.getenv('GOOGLE_ADS_REFRESH_TOKEN')
    GOOGLE_ADS_LOGIN_CUSTOMER_ID = os.getenv('GOOGLE_ADS_LOGIN_CUSTOMER_ID')
    
    # Memory Configuration
    EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
    EMBEDDING_DIMENSION = 384
    MAX_MEMORY_RETRIEVAL = 10
    
    # Agent Configuration
    MAX_ITERATIONS = 3
    MAX_EXECUTION_TIME = 300
    VERBOSE = True
    
    # Campaign Configuration
    DEFAULT_BUDGET = 1000
    DEFAULT_TARGET_ROAS = 400
    DEFAULT_CPC_BID = 2.50
    
    # File Paths
    OUTPUT_DIR = "outputs"
    LOGS_DIR = "logs"
    
    @classmethod
    def validate_config(cls):
        """Validate configuration and provide helpful warnings for optional services"""
        warnings = []
        errors = []
        
        # Check for LLM configuration
        if not os.getenv('OPENAI_API_KEY') and not os.getenv('OLLAMA_BASE_URL'):
            warnings.append("No LLM configured. Set either OPENAI_API_KEY or OLLAMA_BASE_URL")
        
        # Check for Pinecone (optional but recommended)
        if not cls.PINECONE_API_KEY:
            warnings.append("PINECONE_API_KEY not set. Memory will use local file storage only")
        
        # Check for Google Ads (optional)
        google_ads_vars = [
            'GOOGLE_ADS_DEVELOPER_TOKEN',
            'GOOGLE_ADS_CLIENT_ID', 
            'GOOGLE_ADS_CLIENT_SECRET',
            'GOOGLE_ADS_REFRESH_TOKEN',
            'GOOGLE_ADS_LOGIN_CUSTOMER_ID'
        ]
        missing_google_ads = [var for var in google_ads_vars if not os.getenv(var)]
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