from flask import Flask, render_template, request, jsonify, redirect, abort
from database import URLDatabase, RateLimiter
from utils import get_client_ip, format_response, handle_errors
import logging
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize database and rate limiter
db = URLDatabase()
rate_limiter = RateLimiter()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('url_shortener_v2.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@app.route('/')
def home():
    """Main page with URL shortening form"""
    return render_template('index.html')


@app.route('/preview/<short_id>')
def preview_url(short_id):
    """Preview URL information"""
    url_data = db.get_url_by_short_id(short_id)
    if not url_data:
        abort(404)
    
    analytics = db.get_analytics(short_id)
    return render_template('preview.html', url_data=url_data, analytics=analytics)


@app.route('/api/urls')
def list_urls():
    """API endpoint to list all URLs"""
    try:
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        urls = db.get_all_urls(limit=limit, offset=offset)
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
        logger.error(f"Error listing URLs: {str(e)}")
        return handle_errors(e)


@app.route('/api/urls/<short_id>/analytics')
def get_url_analytics(short_id):
    """Get detailed analytics for a URL"""
    try:
        analytics = db.get_analytics(short_id)
        if not analytics:
            return format_response({'status': 'error', 'message': 'URL not found'}, 404)
        
        return format_response({
            'status': 'success',
            'data': analytics
        })
    except Exception as e:
        logger.error(f"Error getting analytics for {short_id}: {str(e)}")
        return handle_errors(e)


@app.route('/api/urls/bulk', methods=['POST'])
def bulk_create_urls():
    """Bulk create multiple shortened URLs"""
    try:
        # Rate limiting
        client_ip = get_client_ip(request)
        if rate_limiter.is_rate_limited(client_ip, '/api/urls/bulk', max_requests=10, window_minutes=1):
            return format_response({'status': 'error', 'message': 'Rate limit exceeded'}, 429)
        
        data = request.get_json()
        if not data or 'urls' not in data:
            return format_response({'status': 'error', 'message': 'Missing URLs data'}, 400)
        
        # Process bulk URLs
        urls_data = []
        for url_item in data['urls']:
            if isinstance(url_item, str):
                urls_data.append({'url': url_item})
            elif isinstance(url_item, dict):
                urls_data.append(url_item)
        
        results = db.bulk_create_urls(
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
        logger.error(f"Error in bulk create: {str(e)}")
        return handle_errors(e)


@app.route('/api/short', methods=['POST'])
def create_short_url():
    """Create a new shortened URL via API"""
    try:
        # Rate limiting
        client_ip = get_client_ip(request)
        if rate_limiter.is_rate_limited(client_ip, '/api/short', max_requests=30, window_minutes=1):
            return format_response({'status': 'error', 'message': 'Rate limit exceeded'}, 429)
        
        data = request.get_json()
        if not data:
            return format_response({'status': 'error', 'message': 'No data provided'}, 400)
        
        # Validate required fields
        required_fields = ['url']
        for field in required_fields:
            if field not in data:
                return format_response({'status': 'error', 'message': f'Missing required field: {field}'}, 400)
        
        # Create URL
        url_data = db.create_short_url(
            original_url=data['url'],
            custom_id=data.get('custom_id'),
            api_key=data.get('api_key', 'default'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            created_by_ip=client_ip,
            expiry_days=data.get('expiry_days', 30)
        )
        
        # Format response
        response_data = {
            'status': 'success',
            'short_link': f"{app.config.get('BASE_URL', 'http://localhost:8398')}/{url_data['short_id']}",
            'id': url_data['short_id'],
            'redirect_link': url_data['original_url'],
            'making_date_time': url_data['creation_time'],
            'expired_time': url_data['expiry_time'],
            'click_count': url_data['click_count'],
            'title': url_data.get('title', ''),
            'description': url_data.get('description', '')
        }
        
        logger.info(f"Created short URL: {url_data['short_id']} for {data['url']}")
        return format_response(response_data)
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return format_response({'status': 'error', 'message': str(e)}, 400)
    except Exception as e:
        logger.error(f"Error creating short URL: {str(e)}")
        return handle_errors(e)


@app.route('/api/short', methods=['GET'])
def create_short_url_get():
    """Create a new shortened URL via GET request"""
    try:
        # Rate limiting
        client_ip = get_client_ip(request)
        if rate_limiter.is_rate_limited(client_ip, '/api/short', max_requests=30, window_minutes=1):
            return format_response({'status': 'error', 'message': 'Rate limit exceeded'}, 429)
        
        # Get parameters
        url = request.args.get('url')
        custom_id = request.args.get('custom_id')
        api_key = request.args.get('api_key', 'default')
        
        if not url:
            return format_response({'status': 'error', 'message': 'Missing url parameter'}, 400)
        
        # Create URL
        url_data = db.create_short_url(
            original_url=url,
            custom_id=custom_id,
            api_key=api_key,
            created_by_ip=client_ip
        )
        
        # Format response
        response_data = {
            'status': 'success',
            'short_link': f"{app.config.get('BASE_URL', 'http://localhost:8398')}/{url_data['short_id']}",
            'id': url_data['short_id'],
            'redirect_link': url_data['original_url'],
            'making_date_time': url_data['creation_time'],
            'expired_time': url_data['expiry_time'],
            'click_count': url_data['click_count']
        }
        
        logger.info(f"Created short URL: {url_data['short_id']} for {url}")
        return format_response(response_data)
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return format_response({'status': 'error', 'message': str(e)}, 400)
    except Exception as e:
        logger.error(f"Error creating short URL: {str(e)}")
        return handle_errors(e)


@app.route('/<short_id>', methods=['GET'])
def redirect_to_url(short_id):
    """Redirect to original URL"""
    try:
        # Get URL data
        url_data = db.get_url_by_short_id(short_id)
        if not url_data:
            logger.warning(f"Short URL not found: {short_id}")
            return jsonify({'status': 'error', 'message': 'Short URL not found'}), 404
        
        # Get analytics data
        client_ip = get_client_ip(request)
        user_agent = request.headers.get('User-Agent', '')
        referrer = request.headers.get('Referer', '')
        
        # Increment click count and log analytics
        db.increment_click_count(short_id, user_agent, referrer, client_ip)
        
        logger.info(f"Redirecting {short_id} to {url_data['original_url']}")
        
        # Redirect to original URL
        return redirect(url_data['original_url'])
        
    except Exception as e:
        logger.error(f"Error redirecting {short_id}: {str(e)}")
        return handle_errors(e)


@app.route('/admin/cleanup', methods=['POST'])
def cleanup_expired_urls():
    """Admin endpoint to cleanup expired URLs"""
    try:
        # Simple admin check (in production, implement proper authentication)
        admin_key = request.headers.get('X-Admin-Key')
        if admin_key != 'admin123':  # Change this in production
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
        deleted_count = db.cleanup_expired_urls()
        
        logger.info(f"Cleaned up {deleted_count} expired URLs")
        return format_response({
            'status': 'success',
            'message': f'Cleaned up {deleted_count} expired URLs'
        })
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        return handle_errors(e)


@app.errorhandler(404)
def not_found(error):
    return format_response({'status': 'error', 'message': 'Not found'}, 404)


@app.errorhandler(500)
def internal_error(error):
    return format_response({'status': 'error', 'message': 'Internal server error'}, 500)


if __name__ == '__main__':
    # Configure base URL
    app.config['BASE_URL'] = 'http://localhost:8398'
    
    # Ensure log file directory exists
    os.makedirs('logs', exist_ok=True)
    
    logger.info("Starting URL Shortener v2.0")
    app.run(debug=True, host='0.0.0.0', port=8398)