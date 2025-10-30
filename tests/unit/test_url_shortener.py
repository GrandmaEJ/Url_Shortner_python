"""Unit tests for URL Shortener v2.0"""

import unittest
import tempfile
import os
from url_shortener import create_app
from url_shortener.config import TestingConfig


class URLShortenerTestCase(unittest.TestCase):
    """Base test case for URL Shortener"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        # Create a test database
        self.db_path = self.app.config['DATABASE_PATH']
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.app_context.pop()
        
        # Clean up test database
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn('healthy', response.get_json()['status'])
    
    def test_api_version(self):
        """Test API version endpoint"""
        response = self.client.get('/api/version')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['version'], '2.0.0')
        self.assertEqual(data['status'], 'active')
    
    def test_create_short_url_post(self):
        """Test creating short URL via POST"""
        test_data = {
            'url': 'https://example.com',
            'custom_id': 'test123'
        }
        
        response = self.client.post('/api/short',
                                 json=test_data,
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['id'], 'test123')
        self.assertIn('short_link', data)
    
    def test_create_short_url_get(self):
        """Test creating short URL via GET"""
        response = self.client.get('/api/short?url=https://example.com&custom_id=test456')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['id'], 'test456')
    
    def test_url_redirection(self):
        """Test URL redirection"""
        # First create a short URL
        test_data = {'url': 'https://example.com', 'custom_id': 'redirect123'}
        create_response = self.client.post('/api/short', json=test_data)
        self.assertEqual(create_response.status_code, 200)
        
        # Then test redirection
        redirect_response = self.client.get('/redirect123')
        self.assertEqual(redirect_response.status_code, 302)
        self.assertIn('https://example.com', redirect_response.location)
    
    def test_get_nonexistent_url(self):
        """Test getting non-existent URL"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()