import os
from typing import Dict, Any


class Config:
    """Application configuration management"""
    
    # Base configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'url_shortener_v2.db'
    
    # URL Shortener specific
    BASE_URL = os.environ.get('BASE_URL') or 'http://localhost:8398'
    DEFAULT_EXPIRY_DAYS = int(os.environ.get('DEFAULT_EXPIRY_DAYS', 30))
    MAX_CUSTOM_ID_LENGTH = int(os.environ.get('MAX_CUSTOM_ID_LENGTH', 20))
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.environ.get('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    RATE_LIMIT_DEFAULT_REQUESTS = int(os.environ.get('RATE_LIMIT_DEFAULT_REQUESTS', 30))
    RATE_LIMIT_BULK_REQUESTS = int(os.environ.get('RATE_LIMIT_BULK_REQUESTS', 10))
    RATE_LIMIT_WINDOW_MINUTES = int(os.environ.get('RATE_LIMIT_WINDOW_MINUTES', 1))
    
    # Admin configuration
    ADMIN_KEY = os.environ.get('ADMIN_KEY') or 'admin123'
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'url_shortener_v2.log'
    
    # Security
    URL_VALIDATION_STRICT = os.environ.get('URL_VALIDATION_STRICT', 'true').lower() == 'true'
    
    @staticmethod
    def init_app(app):
        """Initialize application with this configuration"""
        # Set Flask configuration
        app.config.update(
            SECRET_KEY=Config.SECRET_KEY,
            DATABASE_PATH=Config.DATABASE_PATH,
            BASE_URL=Config.BASE_URL,
            DEFAULT_EXPIRY_DAYS=Config.DEFAULT_EXPIRY_DAYS,
            MAX_CUSTOM_ID_LENGTH=Config.MAX_CUSTOM_ID_LENGTH,
            RATE_LIMIT_ENABLED=Config.RATE_LIMIT_ENABLED,
            RATE_LIMIT_DEFAULT_REQUESTS=Config.RATE_LIMIT_DEFAULT_REQUESTS,
            RATE_LIMIT_BULK_REQUESTS=Config.RATE_LIMIT_BULK_REQUESTS,
            RATE_LIMIT_WINDOW_MINUTES=Config.RATE_LIMIT_WINDOW_MINUTES,
            ADMIN_KEY=Config.ADMIN_KEY,
            LOG_LEVEL=Config.LOG_LEVEL,
            LOG_FILE=Config.LOG_FILE,
            URL_VALIDATION_STRICT=Config.URL_VALIDATION_STRICT
        )


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    
    # Override for production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'prod-secret-change-me'
    BASE_URL = os.environ.get('BASE_URL') or 'https://your-domain.com'
    ADMIN_KEY = os.environ.get('ADMIN_KEY') or 'change-admin-key'
    
    # More restrictive rate limits
    RATE_LIMIT_DEFAULT_REQUESTS = 20
    RATE_LIMIT_BULK_REQUESTS = 5


class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = False
    TESTING = True
    
    # Use in-memory database for testing
    DATABASE_PATH = ':memory:'
    
    # Disable rate limiting for tests
    RATE_LIMIT_ENABLED = False
    
    # Test-specific configuration
    BASE_URL = 'http://localhost:5000'


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}