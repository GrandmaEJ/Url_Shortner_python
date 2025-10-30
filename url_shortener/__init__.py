"""
URL Shortener v2.0 - Professional Package Structure

This package provides a complete URL shortening service with analytics,
bulk operations, and enterprise-grade features.
"""

from .config import Config
from .app import create_app

__version__ = "2.0.0"
__author__ = "URL Shortener Team"

__all__ = ['create_app', 'Config']