import datetime
import json
import logging
from typing import Dict, Any, Optional
from flask import request


def get_client_ip(request) -> str:
    """Get client IP address from request"""
    if request.headers.get('X-Forwarded-For'):
        # If behind a proxy, use the first IP
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr or '0.0.0.0'


def format_response(data: Dict[str, Any], status_code: int = 200) -> tuple:
    """Format API response consistently"""
    return (data, status_code)


def handle_errors(error: Exception) -> tuple:
    """Handle exceptions and format error responses"""
    logging.error(f"Error occurred: {str(error)}")
    return format_response({
        'status': 'error',
        'message': 'An internal error occurred',
        'timestamp': datetime.datetime.now().isoformat()
    }, 500)


def validate_url(url: str) -> bool:
    """Validate URL format"""
    import validators
    return validators.url(url)


def generate_short_id(url: str) -> str:
    """Generate a short ID from URL (legacy function for compatibility)"""
    import hashlib
    return hashlib.md5(url.encode()).hexdigest()[:6]


def format_datetime(dt: datetime.datetime) -> str:
    """Format datetime for JSON response"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_url_info_from_db(short_id: str, db) -> Optional[Dict[str, Any]]:
    """Get URL information from database (legacy compatibility)"""
    return db.get_url_by_short_id(short_id)


def url_expired(expiry_time: str) -> bool:
    """Check if URL has expired (legacy compatibility)"""
    try:
        expiry_dt = datetime.datetime.fromisoformat(expiry_time.replace('Z', '+00:00'))
        return datetime.datetime.now() > expiry_dt
    except:
        return True


def log_missing_params():
    """Log missing parameters (legacy compatibility)"""
    logging.warning(f"Missing parameters: {datetime.datetime.now()}")


def load_data() -> Dict:
    """Load data from JSON file (legacy compatibility)"""
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data(data: Dict):
    """Save data to JSON file (legacy compatibility)"""
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)


def create_error_response(message: str, status_code: int = 400) -> tuple:
    """Create standardized error response"""
    return format_response({
        'status': 'error',
        'message': message,
        'timestamp': datetime.datetime.now().isoformat()
    }, status_code)


def create_success_response(data: Any, message: str = "Success") -> tuple:
    """Create standardized success response"""
    return format_response({
        'status': 'success',
        'message': message,
        'data': data,
        'timestamp': datetime.datetime.now().isoformat()
    })


def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    if not text:
        return ""
    # Remove potentially dangerous characters
    sanitized = ''.join(char for char in text if char.isalnum() or char in '-_/.')
    return sanitized.strip()


def is_valid_custom_id(custom_id: str) -> bool:
    """Validate custom ID format"""
    if not custom_id:
        return True  # Empty is valid (will auto-generate)
    
    # Check length
    if len(custom_id) < 3 or len(custom_id) > 20:
        return False
    
    # Check characters (alphanumeric and dashes/underscores only)
    import re
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', custom_id))


def get_request_info(request) -> Dict[str, str]:
    """Get request information for logging"""
    return {
        'ip': get_client_ip(request),
        'user_agent': request.headers.get('User-Agent', ''),
        'method': request.method,
        'url': request.url,
        'referrer': request.headers.get('Referer', '')
    }


class URLValidator:
    """URL validation utilities"""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if URL is valid"""
        if not url or not isinstance(url, str):
            return False
        
        import validators
        return validators.url(url)
    
    @staticmethod
    def is_safe_url(url: str) -> bool:
        """Check if URL is safe (not javascript:, data:, etc.)"""
        if not url:
            return False
        
        url_lower = url.lower().strip()
        unsafe_protocols = ['javascript:', 'data:', 'vbscript:', 'file:', 'about:']
        
        return not any(url_lower.startswith(protocol) for protocol in unsafe_protocols)
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalize URL"""
        if not url:
            return ""
        
        url = url.strip()
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return url


class AnalyticsHelper:
    """Analytics and tracking utilities"""
    
    @staticmethod
    def get_browser_info(user_agent: str) -> str:
        """Extract browser information from user agent"""
        if not user_agent:
            return "Unknown"
        
        user_agent = user_agent.lower()
        
        if 'chrome' in user_agent:
            return "Chrome"
        elif 'firefox' in user_agent:
            return "Firefox"
        elif 'safari' in user_agent:
            return "Safari"
        elif 'edge' in user_agent:
            return "Edge"
        elif 'opera' in user_agent:
            return "Opera"
        else:
            return "Other"
    
    @staticmethod
    def get_device_info(user_agent: str) -> str:
        """Extract device information from user agent"""
        if not user_agent:
            return "Unknown"
        
        user_agent = user_agent.lower()
        
        if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
            return "Mobile"
        elif 'tablet' in user_agent or 'ipad' in user_agent:
            return "Tablet"
        else:
            return "Desktop"