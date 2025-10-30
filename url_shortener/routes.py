from flask import Blueprint, render_template, request, jsonify, redirect, abort
from .services import URLService, AnalyticsService
from .utils import get_client_ip, validate_required_fields


# Create blueprints
api_bp = Blueprint('api', __name__, url_prefix='/api')
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Main page with URL shortening form"""
    return render_template('index.html')


@main_bp.route('/preview/<short_id>')
def preview_url(short_id):
    """Preview URL information"""
    url_data = url_service.get_url_by_short_id(short_id)
    if not url_data:
        abort(404)
    
    analytics = url_service.url_service.url_model.get_analytics(short_id)
    return render_template('preview.html', url_data=url_data, analytics=analytics)


@main_bp.route('/admin/cleanup', methods=['POST'])
def cleanup_expired_urls():
    """Admin endpoint to cleanup expired URLs"""
    try:
        # Simple admin check (in production, implement proper authentication)
        admin_key = request.headers.get('X-Admin-Key')
        if admin_key != url_service.config.ADMIN_KEY:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
        result = url_service.cleanup_expired_urls(admin_key)
        return result
        
    except Exception as e:
        from .utils import handle_errors
        return handle_errors(e)


# URL Shortening Routes
@api_bp.route('/urls')
def list_urls():
    """API endpoint to list all URLs"""
    try:
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        result = url_service.get_all_urls(limit=limit, offset=offset)
        return result
        
    except Exception as e:
        from .utils import handle_errors
        return handle_errors(e)


@api_bp.route('/urls/<short_id>/analytics')
def get_url_analytics(short_id):
    """Get detailed analytics for a URL"""
    try:
        result = analytics_service.get_comprehensive_analytics(short_id)
        return result
    except Exception as e:
        from .utils import handle_errors
        return handle_errors(e)


@api_bp.route('/urls/bulk', methods=['POST'])
def bulk_create_urls():
    """Bulk create multiple shortened URLs"""
    try:
        data = request.get_json()
        if not data:
            from .utils import create_error_response
            return create_error_response('No data provided', 400)
        
        result = url_service.bulk_create_urls(data, request)
        return result
        
    except Exception as e:
        from .utils import handle_errors
        return handle_errors(e)


@api_bp.route('/short', methods=['POST'])
def create_short_url():
    """Create a new shortened URL via API"""
    try:
        data = request.get_json()
        if not data:
            from .utils import create_error_response
            return create_error_response('No data provided', 400)
        
        result = url_service.create_short_url(data, request)
        return result
        
    except Exception as e:
        from .utils import handle_errors
        return handle_errors(e)


@api_bp.route('/short', methods=['GET'])
def create_short_url_get():
    """Create a new shortened URL via GET request"""
    try:
        # Get parameters
        url = request.args.get('url')
        custom_id = request.args.get('custom_id')
        api_key = request.args.get('api_key', 'default')
        
        if not url:
            from .utils import create_error_response
            return create_error_response('Missing url parameter', 400)
        
        # Create URL
        data = {
            'url': url,
            'custom_id': custom_id,
            'api_key': api_key
        }
        
        result = url_service.create_short_url(data, request)
        return result
        
    except Exception as e:
        from .utils import handle_errors
        return handle_errors(e)


# Redirection route (outside API blueprint since it's the main functionality)
@main_bp.route('/<short_id>', methods=['GET'])
def redirect_to_url(short_id):
    """Redirect to original URL"""
    try:
        result = url_service.redirect_to_url(short_id, request)
        return result[0] if isinstance(result, tuple) else result
        
    except Exception as e:
        from .utils import handle_errors
        return handle_errors(e)


# Error handlers
@main_bp.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Not found'}), 404


@main_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500


# Initialize services (will be set by app factory)
url_service = None
analytics_service = None


def init_services(config):
    """Initialize services with configuration"""
    global url_service, analytics_service
    url_service = URLService(config)
    analytics_service = AnalyticsService(url_service)


def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)