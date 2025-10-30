# 🚀 URL Shortener v2.0 - Enterprise Grade Solution

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-2.0-success.svg)

**🚀 Enterprise-grade URL shortening service with analytics, bulk operations, and advanced features**

[✨ What's New in v2.0](#-whats-new-in-v20) • [🏃‍♂️ Quick Start](#-quick-start) • [📖 API Documentation](#-api-documentation) • [🎯 Examples](#-examples) • [🛠️ Development](#-development)

</div>

---

## ✨ What's New in v2.0

### 🆕 Major Features Added
- 🔗 **Smart Analytics** - Real-time click tracking with browser and referrer analysis
- 📊 **Preview Dashboard** - Beautiful URL preview pages with detailed analytics
- ⚡ **Bulk Operations** - Shorten multiple URLs simultaneously via API
- 🛡️ **Advanced Security** - Rate limiting, URL validation, and input sanitization
- 🏪 **SQLite Database** - Reliable data persistence with structured storage
- 🎯 **Enhanced Custom IDs** - Support for titles, descriptions, and metadata
- 📈 **Analytics API** - Detailed statistics and reporting endpoints
- 🔄 **Improved Performance** - Optimized database queries and caching

### 🆚 v1.0 vs v2.0 Comparison

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Storage | JSON File | SQLite Database |
| Analytics | None | Real-time tracking |
| Bulk Operations | ❌ | ✅ |
| Rate Limiting | ❌ | ✅ |
| URL Preview | ❌ | ✅ |
| API Endpoints | 2 | 6+ |
| Security | Basic | Enterprise-grade |
| Custom Metadata | ❌ | ✅ |

---

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/GrandmaEJ/api.git
   cd simple-url-shortener
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database** (auto-created on first run)
   ```bash
   python index.py
   ```

4. **Access the application**
   - 🌐 **Web Interface**: `http://localhost:8398`
   - 🔗 **API Base URL**: `http://localhost:8398/api`
   - 👁️ **Preview URL**: `http://localhost:8398/preview/<short_id>`

---

## 📖 API Documentation

### Base Configuration
- **Base URL**: `http://localhost:8398`
- **API Version**: `v2.0`
- **Content-Type**: `application/json`

### 🔗 Core Endpoints

#### 1. Create Short URL (POST)
Create a new shortened URL with advanced options.

**Endpoint**: `POST /api/short`

**Request Body**:
```json
{
    "url": "https://example.com/very/long/url",
    "custom_id": "mycustom",        // Optional
    "title": "My Website",          // Optional
    "description": "Main website",  // Optional
    "expiry_days": 30               // Optional (default: 30)
}
```

**Response**:
```json
{
    "status": "success",
    "short_link": "http://localhost:8398/mycustom",
    "id": "mycustom",
    "redirect_link": "https://example.com/very/long/url",
    "making_date_time": "2025-10-30 06:43:31",
    "expired_time": "2025-11-29 06:43:31",
    "click_count": 0,
    "title": "My Website",
    "description": "Main website"
}
```

#### 2. Create Short URL (GET)
Create a short URL using query parameters.

**Endpoint**: `GET /api/short?url=<url>&custom_id=<id>`

#### 3. Bulk URL Creation
Create multiple shortened URLs at once.

**Endpoint**: `POST /api/urls/bulk`

**Request Body**:
```json
{
    "urls": [
        "https://example.com",
        {"url": "https://google.com", "custom_id": "google"},
        {"url": "https://github.com", "title": "GitHub"}
    ]
}
```

#### 4. URL Analytics
Get detailed analytics for a shortened URL.

**Endpoint**: `GET /api/urls/<short_id>/analytics`

**Response**:
```json
{
    "status": "success",
    "data": {
        "url_info": {
            "short_id": "abc123",
            "original_url": "https://example.com",
            "click_count": 42,
            "creation_time": "2025-10-30 06:43:31"
        },
        "daily_clicks": [
            {"date": "2025-10-30", "clicks": 15},
            {"date": "2025-10-29", "clicks": 27}
        ],
        "user_agents": [
            {"user_agent": "Chrome", "clicks": 30},
            {"user_agent": "Safari", "clicks": 12}
        ],
        "referrers": [
            {"referrer": "https://google.com", "clicks": 25},
            {"referrer": "https://twitter.com", "clicks": 10}
        ]
    }
}
```

#### 5. List All URLs
Retrieve paginated list of all shortened URLs.

**Endpoint**: `GET /api/urls?limit=50&offset=0`

#### 6. Redirect Endpoint
Redirect users from short URL to original URL.

**Endpoint**: `GET /<short_id>`

### 🛡️ Security Features

#### Rate Limiting
- **Default Limits**: 30 requests/minute for URL creation
- **Bulk Operations**: 10 requests/minute
- **Headers**: `X-RateLimit-Remaining`, `X-RateLimit-Reset`

#### URL Validation
- **Format**: Strict URL format validation
- **Safety**: Blocks dangerous protocols (javascript:, data:, etc.)
- **Normalization**: Automatic protocol addition (http/https)

---

## 🎯 Examples

### Using the Web Interface
1. Navigate to `http://localhost:8398`
2. Enter your long URL
3. Optionally add custom ID, title, and description
4. Click "Shorten URL"
5. View result with copy and preview options

### API Examples

#### cURL Examples
```bash
# Create single URL
curl -X POST http://localhost:8398/api/short \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com/python/cpython",
    "custom_id": "pyrepo",
    "title": "Python CPython",
    "description": "Python interpreter source code"
  }'

# Bulk creation
curl -X POST http://localhost:8398/api/urls/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://www.python.org/",
      {"url": "https://docs.python.org/", "custom_id": "pydocs"},
      {"url": "https://pypi.org/", "title": "PyPI"}
    ]
  }'

# Get analytics
curl http://localhost:8398/api/urls/pyrepo/analytics
```

#### JavaScript Examples
```javascript
// Create short URL
const response = await fetch('/api/short', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        url: 'https://example.com',
        custom_id: 'example',
        title: 'My Example Site'
    })
});
const result = await response.json();

// Bulk creation
const bulkResponse = await fetch('/api/urls/bulk', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        urls: [
            'https://site1.com',
            'https://site2.com',
            {url: 'https://site3.com', custom_id: 'site3'}
        ]
    })
});
```

#### Python Examples
```python
import requests

# Single URL creation
response = requests.post('http://localhost:8398/api/short', json={
    'url': 'https://www.python.org/',
    'custom_id': 'python',
    'title': 'Python Official Website',
    'description': 'Home of the Python programming language'
})

data = response.json()
print(f"Short link: {data['short_link']}")

# Bulk creation
bulk_response = requests.post('http://localhost:8398/api/urls/bulk', json={
    'urls': [
        'https://docs.python.org/',
        {'url': 'https://pypi.org/', 'title': 'Python Package Index'}
    ]
})

bulk_data = bulk_response.json()
print(f"Created {bulk_data['successful']} URLs")
```

---

## 🛠️ Development

### Project Structure
```
Url_Shortner_python/
├── 📄 index.py              # Main Flask application (v2.0)
├── 📄 database.py           # Database management and operations
├── 📄 utils.py              # Enhanced utilities and helpers
├── 📄 requirements.txt      # Python dependencies
├── 📁 templates/
│   ├── 📄 index.html       # Modern web interface
│   └── 📄 preview.html     # URL preview page
├── 📁 static/
│   ├── 📁 css/
│   │   ├── 📄 styles.css   # Main styling
│   │   └── 📄 preview.css  # Preview page styling
│   └── 📁 js/
│       └── 📄 main.js      # Enhanced frontend JavaScript
└── 📄 README.md            # This file
```

### Database Schema

#### `urls` Table
```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_id TEXT UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    custom_id TEXT UNIQUE,
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_time TIMESTAMP NOT NULL,
    click_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    api_key TEXT,
    title TEXT,
    description TEXT,
    created_by_ip TEXT
);
```

#### `click_analytics` Table
```sql
CREATE TABLE click_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_id TEXT NOT NULL,
    click_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_agent TEXT,
    referrer TEXT,
    ip_address TEXT,
    FOREIGN KEY (short_id) REFERENCES urls (short_id)
);
```

#### `rate_limit` Table
```sql
CREATE TABLE rate_limit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    request_count INTEGER DEFAULT 1,
    window_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Configuration

#### Environment Variables
```bash
# Database Configuration
DATABASE_URL=url_shortener_v2.db

# Security Configuration
SECRET_KEY=your-secret-key
ADMIN_KEY=your-admin-key

# Rate Limiting
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=url_shortener_v2.log
```

#### Custom Settings
```python
# In index.py
app.config.update(
    SECRET_KEY='your-secret-key',
    BASE_URL='https://your-domain.com',  # Change for production
    DATABASE_URL='url_shortener_v2.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
```

### Performance Features
- **Database Indexing**: Optimized queries on short_id and click_time
- **Connection Pooling**: Efficient database connections
- **Rate Limiting**: Built-in request throttling
- **Caching**: Response caching for analytics endpoints
- **Cleanup Jobs**: Automatic expired URL cleanup

---

## 🔧 Troubleshooting

### Common Issues

#### Database Errors
```bash
# Reset database
rm url_shortener_v2.db
python index.py  # Will recreate database
```

#### Port Conflicts
```python
# Change port in index.py
app.run(debug=True, host='0.0.0.0', port=8399)
```

#### Permission Issues
```bash
# Ensure write permissions
chmod 664 url_shortener_v2.db *.log
```

#### Rate Limiting
```python
# Adjust limits in database.py
rate_limiter = RateLimiter()
# Modify max_requests in is_rate_limited() calls
```

### Debug Mode
```bash
# Enable debug logging
export FLASK_DEBUG=1
export LOG_LEVEL=DEBUG
python index.py
```

### Health Check
```bash
# Test API endpoints
curl http://localhost:8398/api/urls?limit=1
```

---

## 🚀 Deployment

### Production Checklist
- [ ] Change `SECRET_KEY` in production
- [ ] Configure proper `BASE_URL`
- [ ] Set up database backups
- [ ] Enable HTTPS
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Configure rate limiting
- [ ] Set up admin authentication

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8398
CMD ["python", "index.py"]
```

### Environment Setup
```bash
# Production environment
export FLASK_ENV=production
export DATABASE_URL=postgresql://user:pass@host/db
python index.py
```

---

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create virtual environment: `python -m venv venv`
3. Activate environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run tests: `python -m pytest`
6. Submit pull request

### Code Standards
- **Python**: Follow PEP 8
- **API**: RESTful design principles
- **Database**: Use migrations for schema changes
- **Testing**: Add tests for new features
- **Documentation**: Update README and API docs

---

## 📈 Roadmap

### v2.1 (Planned)
- [ ] User authentication system
- [ ] Custom domains
- [ ] QR code generation
- [ ] Advanced analytics dashboard
- [ ] API key management

### v2.2 (Future)
- [ ] Multiple database support (PostgreSQL, MySQL)
- [ ] Redis caching layer
- [ ] Load balancing support
- [ ] Advanced user roles
- [ ] Bulk import/export

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

### Getting Help
- 📧 **Issues**: [GitHub Issues](https://github.com/GrandmaEJ/api/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/GrandmaEJ/api/discussions)
- 📖 **Wiki**: [Project Wiki](https://github.com/GrandmaEJ/api/wiki)

### Community
- ⭐ **Star** this repository if you find it helpful
- 🐛 **Report bugs** via GitHub Issues
- 💡 **Suggest features** via GitHub Discussions
- 🤝 **Contribute** by submitting pull requests

---

<div align="center">

**Made with ❤️ using Python, Flask, and SQLite**

[⬆ Back to Top](#-url-shortener-v20---enterprise-grade-solution)

**🚀 URL Shortener v2.0 - Now with Analytics, Bulk Operations, and Enterprise Features!**

</div>
