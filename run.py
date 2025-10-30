#!/usr/bin/env python3
"""
URL Shortener v2.0 - Professional CLI Entry Point

This is the main entry point for the URL Shortener application.
Run this script to start the server.
"""

import os
import sys
import click
from flask.cli import FlaskGroup
from url_shortener import create_app


def create_cli_app():
    """Create CLI app for management commands"""
    return create_app()


@click.group(cls=FlaskGroup, create_app=create_cli_app)
def cli():
    """URL Shortener v2.0 Management Commands"""
    pass


@cli.command()
@click.option('--host', '-h', default='0.0.0.0', help='Host to bind to')
@click.option('--port', '-p', default=8398, help='Port to bind to')
@click.option('--debug', '-d', is_flag=True, help='Enable debug mode')
@click.option('--config', '-c', default='development', help='Configuration to use')
def run(host, port, debug, config):
    """Run the development server"""
    os.environ['FLASK_ENV'] = 'development' if debug else 'production'
    app = create_app(config)
    
    click.echo(f"🚀 Starting URL Shortener v2.0 on {host}:{port}")
    click.echo(f"📖 Configuration: {config}")
    click.echo(f"🌐 Base URL: {app.config.get('BASE_URL', 'http://localhost:8398')}")
    
    app.run(host=host, port=port, debug=debug)


@cli.command()
def test():
    """Run tests"""
    import unittest
    from tests.unit.test_url_shortener import URLShortenerTestCase
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(URLShortenerTestCase)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        click.echo("✅ All tests passed!")
        sys.exit(0)
    else:
        click.echo("❌ Some tests failed!")
        sys.exit(1)


@cli.command()
@click.option('--config', '-c', default='development', help='Configuration to use')
def init_db(config):
    """Initialize the database"""
    from url_shortener.models import URLModel
    
    app = create_app(config)
    
    with app.app_context():
        db_path = app.config['DATABASE_PATH']
        url_model = URLModel(db_path)
        url_model.init_database()
        
        click.echo(f"✅ Database initialized: {db_path}")


@cli.command()
@click.option('--config', '-c', default='development', help='Configuration to use')
def cleanup_expired(config):
    """Cleanup expired URLs"""
    from url_shortener.services import URLService
    
    app = create_app(config)
    
    with app.app_context():
        url_service = URLService(app.config)
        result = url_service.cleanup_expired_urls(app.config['ADMIN_KEY'])
        
        if isinstance(result, tuple):
            data, status = result
            if data.get('status') == 'success':
                click.echo(f"✅ {data['message']}")
            else:
                click.echo(f"❌ {data['message']}")
        else:
            click.echo(f"✅ Cleanup completed")


if __name__ == '__main__':
    cli()