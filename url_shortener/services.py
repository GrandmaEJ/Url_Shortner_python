import logging
from typing import Dict, Any, Optional
from .models import URLModel, RateLimitModel
from .utils import get_client_ip, format_response, handle_errors, URLValidator


class URLService:
    """Service layer for URL shortening operations"""
    
    def __init__(self, config_dict):
        self.url_model = URLModel(config_dict['DATABASE_PATH'])
        self.rate_model = RateLimitModel(config_dict['DATABASE_PATH'])
        self.config = config_dict
        self.logger = logging.getLogger(__name__)
    
    def create_short_url(self, data: Dict[str, Any], request=None) -> Dict[str, Any]:
        """Create a new shortened URL with validation and rate limiting"""
        try:
            # Rate limiting
            if self.config['RATE_LIMIT_ENABLED'] and request:
                client_ip = get_client_ip(request)
                if self.rate_model.is_rate_limited(
                    client_ip, '/api/short', 
                    self.config['RATE_LIMIT_DEFAULT_REQUESTS'], 
                    self.config['RATE_LIMIT_WINDOW_MINUTES']
                ):
                    return format_response({'status': 'error', 'message': 'Rate limit exceeded'}, 429)
            
            # Validate required fields
            if 'url' not in data:
                return format_response({'status': 'error', 'message': 'Missing required field: url'}, 400)
            
            original_url = data['url']
            custom_id = data.get('custom_id')
            api_key = data.get('api_key', 'default')
            title = data.get('title', '')
            description = data.get('description', '')
            expiry_days = data.get('expiry_days', self.config['DEFAULT_EXPIRY_DAYS'])
            
            # Validate URL
            if not URLValidator.is_valid_url(original_url):
                return format_response({'status': 'error', 'message': 'Invalid URL format'}, 400)
            
            if not URLValidator.is_safe_url(original_url):
                return format_response({'status': 'error', 'message': 'URL is not safe'}, 400)
            
            # Normalize URL
            original_url = URLValidator.normalize_url(original_url)
            
            # Validate custom ID
            if custom_id and not self._validate_custom_id(custom_id):
                return format_response({'status': 'error', 'message': 'Invalid custom ID format'}, 400)
            
            # Get client IP
            created_by_ip = get_client_ip(request) if request else ""
            
            # Create URL
            url_data = self.url_model.create_short_url(
                original_url=original_url,
                custom_id=custom_id,
                api_key=api_key,
                title=title,
                description=description,
                created_by_ip=created_by_ip,
                expiry_days=expiry_days
            )
            
            # Format response
            response_data = {
                'status': 'success',
                'short_link': f"{self.config['BASE_URL']}/{url_data['short_id']}",
                'id': url_data['short_id'],
                'redirect_link': url_data['original_url'],
                'making_date_time': url_data['creation_time'],
                'expired_time': url_data['expiry_time'],
                'click_count': url_data['click_count'],
                'title': url_data.get('title', ''),
                'description': url_data.get('description', '')
            }
            
            self.logger.info(f"Created short URL: {url_data['short_id']} for {original_url}")
            return format_response(response_data)
            
        except ValueError as e:
            self.logger.warning(f"Validation error: {str(e)}")
            return format_response({'status': 'error', 'message': str(e)}, 400)
        except Exception as e:
            self.logger.error(f"Error creating short URL: {str(e)}")
            return handle_errors(e)
    
    def get_url_by_short_id(self, short_id: str) -> Optional[Dict[str, Any]]:
        """Get URL data by short ID"""
        return self.url_model.get_url_by_short_id(short_id)
    
    def redirect_to_url(self, short_id: str, request) -> tuple:
        """Handle URL redirection with analytics"""
        try:
            # Get URL data
            url_data = self.get_url_by_short_id(short_id)
            if not url_data:
                self.logger.warning(f"Short URL not found: {short_id}")
                return format_response({'status': 'error', 'message': 'Short URL not found'}, 404)
            
            # Get analytics data
            client_ip = get_client_ip(request)
            user_agent = request.headers.get('User-Agent', '')
            referrer = request.headers.get('Referer', '')
            
            # Increment click count and log analytics
            self.url_model.increment_click_count(short_id, user_agent, referrer, client_ip)
            
            self.logger.info(f"Redirecting {short_id} to {url_data['original_url']}")
            
            # Return redirect tuple
            from flask import redirect
            return (redirect(url_data['original_url']),)
            
        except Exception as e:
            self.logger.error(f"Error redirecting {short_id}: {str(e)}")
            return handle_errors(e)
    
    def get_url_analytics(self, short_id: str) -> Dict[str, Any]:
        """Get detailed analytics for a URL"""
        try:
            analytics = self.url_model.get_analytics(short_id)
            if not analytics:
                return format_response({'status': 'error', 'message': 'URL not found'}, 404)
            
            return format_response({
                'status': 'success',
                'data': analytics
            })
        except Exception as e:
            self.logger.error(f"Error getting analytics for {short_id}: {str(e)}")
            return handle_errors(e)
    
    def bulk_create_urls(self, data: Dict[str, Any], request=None) -> Dict[str, Any]:
        """Create multiple shortened URLs at once"""
        try:
            # Rate limiting
            if self.config['RATE_LIMIT_ENABLED'] and request:
                client_ip = get_client_ip(request)
                if self.rate_model.is_rate_limited(
                    client_ip, '/api/urls/bulk', 
                    self.config['RATE_LIMIT_BULK_REQUESTS'], 
                    self.config['RATE_LIMIT_WINDOW_MINUTES']
                ):
                    return format_response({'status': 'error', 'message': 'Rate limit exceeded'}, 429)
            
            # Validate data
            if 'urls' not in data:
                return format_response({'status': 'error', 'message': 'Missing URLs data'}, 400)
            
            # Process bulk URLs
            urls_data = []
            for url_item in data['urls']:
                if isinstance(url_item, str):
                    urls_data.append({'url': url_item})
                elif isinstance(url_item, dict):
                    urls_data.append(url_item)
            
            # Get client IP
            created_by_ip = get_client_ip(request) if request else ""
            for url_data in urls_data:
                url_data['created_by_ip'] = created_by_ip
            
            results = self.url_model.bulk_create_urls(
                urls_data=urls_data,
                api_key=data.get('api_key', 'default')
            )
            
            return format_response({
                'status': 'success',
                'data': results,
                'total_processed': len(urls_data),
                'successful': len([r for r in results if 'error' not in r])
            })
            
        except Exception as e:
            self.logger.error(f"Error in bulk create: {str(e)}")
            return handle_errors(e)
    
    def get_all_urls(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Get all URLs with pagination"""
        try:
            urls = self.url_model.get_all_urls(limit=limit, offset=offset)
            return format_response({
                'status': 'success',
                'data': urls,
                'pagination': {
                    'limit': limit,
                    'offset': offset,
                    'count': len(urls)
                }
            })
        except Exception as e:
            self.logger.error(f"Error listing URLs: {str(e)}")
            return handle_errors(e)
    
    def cleanup_expired_urls(self, admin_key: str) -> Dict[str, Any]:
        """Admin function to cleanup expired URLs"""
        try:
            # Simple admin check
            if admin_key != self.config['ADMIN_KEY']:
                return format_response({'status': 'error', 'message': 'Unauthorized'}, 401)
            
            deleted_count = self.url_model.cleanup_expired_urls()
            
            self.logger.info(f"Cleaned up {deleted_count} expired URLs")
            return format_response({
                'status': 'success',
                'message': f'Cleaned up {deleted_count} expired URLs'
            })
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")
            return handle_errors(e)
    
    def _validate_custom_id(self, custom_id: str) -> bool:
        """Validate custom ID format"""
        if not custom_id:
            return True  # Empty is valid (will auto-generate)
        
        # Check length
        if len(custom_id) < 3 or len(custom_id) > self.config['MAX_CUSTOM_ID_LENGTH']:
            return False
        
        # Check characters (alphanumeric and dashes/underscores only)
        import re
        return bool(re.match(r'^[a-zA-Z0-9_-]+$', custom_id))


class AnalyticsService:
    """Service layer for analytics operations"""
    
    def __init__(self, url_service: URLService):
        self.url_service = url_service
        self.logger = logging.getLogger(__name__)
    
    def get_comprehensive_analytics(self, short_id: str) -> Dict[str, Any]:
        """Get comprehensive analytics for a URL"""
        try:
            # Get basic analytics
            analytics_result = self.url_service.get_url_analytics(short_id)
            if isinstance(analytics_result, tuple):
                return analytics_result[0] if analytics_result[0].get('status') == 'error' else analytics_result[0]
            
            if analytics_result.get('status') != 'success':
                return analytics_result
            
            analytics_data = analytics_result['data']
            
            # Add computed metrics
            if analytics_data.get('daily_clicks'):
                total_clicks = sum(day['clicks'] for day in analytics_data['daily_clicks'])
                analytics_data['total_clicks'] = total_clicks
                analytics_data['unique_days'] = len(analytics_data['daily_clicks'])
            
            if analytics_data.get('user_agents'):
                # Get browser type breakdown
                browser_types = {}
                for ua_data in analytics_data['user_agents']:
                    user_agent = ua_data['user_agent']
                    browser = self._extract_browser_type(user_agent)
                    browser_types[browser] = browser_types.get(browser, 0) + ua_data['clicks']
                
                analytics_data['browser_types'] = [
                    {'browser': browser, 'clicks': clicks} 
                    for browser, clicks in sorted(browser_types.items(), key=lambda x: x[1], reverse=True)
                ]
            
            return format_response({
                'status': 'success',
                'data': analytics_data
            })
            
        except Exception as e:
            self.logger.error(f"Error getting comprehensive analytics for {short_id}: {str(e)}")
            return handle_errors(e)
    
    def _extract_browser_type(self, user_agent: str) -> str:
        """Extract browser type from user agent"""
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