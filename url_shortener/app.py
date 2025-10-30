import logging
import os
from flask import Flask
from .config import config
from .routes import register_blueprints, init_services


def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    config_class = config[config_name]
    app.config.from_object(config_class)
    config_class.init_app(app)
    
    # Configure logging
    configure_logging(app)
    
    # Initialize services
    init_services(app.config)
    
    # Register blueprints
    register_blueprints(app)
    
    # Configure static and template directories (for development)
    # In production, these should be in the package
    if os.path.exists('templates'):
        app.template_folder = 'templates'
    if os.path.exists('static'):
        app.static_folder = 'static'
    
    # Add configuration to template context
    @app.context_processor
    def inject_config():
        return {'config': app.config}
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'version': '2.0.0'}, 200
    
    # API version endpoint
    @app.route('/api/version')
    def api_version():
        return {'version': '2.0.0', 'status': 'active'}, 200
    
    app.logger.info("URL Shortener v2.0 initialized successfully")
    return app


def configure_logging(app):
    """Configure application logging"""
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging level
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper())
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    log_file = app.config.get('LOG_FILE', 'url_shortener_v2.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Configure Flask logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)