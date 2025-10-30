# 🚀 URL Shortener v2.0 - Professional Python Package

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-2.0-success.svg)
![Package](https://img.shields.io/badge/Package-PyPI-blue?logo=pypi&logoColor=white)

**Professional URL shortening service with analytics, bulk operations, and enterprise features**
**Organized as a Python package with CLI management tools**

[🏗️ Architecture](#-architecture) • [🚀 Quick Start](#-quick-start) • [🛠️ CLI Commands](#-cli-commands) • [📖 API Documentation](#-api-documentation) • [🧪 Development](#-development)

</div>

---

## 🏗️ Architecture

### Package Structure
The codebase has been reorganized into a professional Python package structure following Flask best practices:

```
Url_Shortner_python/
├── 📁 url_shortener/              # Main Python package
│   ├── 📄 __init__.py            # Package initialization
│   ├── 📄 app.py                 # Flask application factory
│   ├── 📄 config.py              # Configuration management
│   ├── 📄 models.py              # Database models & operations
│   ├── 📄 services.py            # Business logic & services
│   ├── 📄 routes.py              # API routes & endpoints
│   ├── 📄 utils.py               # Utility functions
│   ├── 📁 templates/             # Jinja2 templates
│   └── 📁 static/                # Static files (CSS, JS)
├── 📁 tests/                     # Test suite
│   ├── 📄 __init__.py
│   └── 📁 unit/                  # Unit tests
│       └── 📄 test_url_shortener.py
├── 📄 run.py                     # CLI entry point
├── 📄 setup.py                   # Package setup configuration
├── 📄 requirements.txt           # Python dependencies
└── 📄 README.md                  # This file
```

### Key Components

#### 🎯 **Models** (`models.py`)
- **URLModel**: Database operations for URL shortening
- **RateLimitModel**: Rate limiting management
- SQLite database with optimized indexes
- Comprehensive analytics tracking

#### ⚙️ **Services** (`services.py`)
- **URLService**: Core URL shortening business logic
- **AnalyticsService**: Advanced analytics processing
- Validation, rate limiting, and error handling
- Separation of business logic from Flask

#### 🛣️ **Routes** (`routes.py`)
- **API Routes**: RESTful API endpoints under `/api/`
- **Web Routes**: HTML templates and web interface
- Blueprint-based organization
- Comprehensive error handling

#### 🔧 **Configuration** (`config.py`)
- **DevelopmentConfig**: Development environment settings
- **ProductionConfig**: Production environment settings  
- **TestingConfig**: Testing environment settings
- Environment-based configuration management

#### 🏭 **App Factory** (`app.py`)
- **create_app()**: Flask application factory pattern
- Blueprint registration
- Logging configuration
- Service initialization

---

## 🚀 Quick Start

### Installation

1. **Clone and setup**
   ```bash
   git clone https://github.com/GrandmaEJ/api.git
   cd Url_Shortner_python
   ```

2. **Install dependencies**
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Or using uv (recommended)
   uv add flask validators click
   ```

3. **Initialize database**
   ```bash
   python run.py init-db
   ```

4. **Start the server**
   ```bash
   python run.py run
   ```

5. **Access the application**
   - 🌐 **Web Interface**: `http://localhost:8398`
   - 🔗 **API Base**: `http://localhost:8398/api`
   - 📊 **Health Check**: `http://localhost:8398/health`

---

## 🛠️ CLI Commands

The application provides comprehensive CLI management commands:

### Server Management
```bash
# Start development server
python run.py run

# Start with custom options
python run.py run --host 0.0.0.0 --port 5000 --debug

# Use specific configuration
python run.py run --config production
```

### Database Management
```bash
# Initialize database
python run.py init-db

# Clean up expired URLs
python run.py cleanup-expired
```

### Testing
```bash
# Run test suite
python run.py test
```

### Help
```bash
# View all available commands
python run.py --help

# View specific command help
python run.py run --help
```

---

## 📖 API Documentation

### Base Configuration
- **Base URL**: `http://localhost:8398`
- **API Version**: `v2.0`
- **Content-Type**: `application/json`

### 🔗 Core Endpoints

#### 1. Create Short URL (POST)
```bash
POST /api/short
Content-Type: application/json

{
    "url": "https://example.com/very/long/url",
    "custom_id": "mycustom",        # Optional
    "title": "My Website",          # Optional
    "description": "Main website",  # Optional
    "expiry_days": 30               # Optional (default: 30)
}
```

#### 2. Bulk URL Creation
```bash
POST /api/urls/bulk
Content-Type: application/json

{
    "urls": [
        "https://example.com",
        {"url": "https://google.com", "custom_id": "google"},
        {"url": "https://github.com", "title": "GitHub"}
    ]
}
```

#### 3. URL Analytics
```bash
GET /api/urls/<short_id>/analytics
```

#### 4. List All URLs
```bash
GET /api/urls?limit=50&offset=0
```

#### 5. Redirect
```bash
GET /<short_id>  # Redirects to original URL
```

### 🔍 Health & Status Endpoints

#### Health Check
```bash
GET /health
Response: {"status": "healthy", "version": "2.0.0"}
```

#### API Version
```bash
GET /api/version
Response: {"version": "2.0.0", "status": "active"}
```

---

## 🎯 Examples

### Using the Web Interface
1. Navigate to `http://localhost:8398`
2. Enter your long URL
3. Optionally add custom ID, title, and description
4. Click "Shorten URL"
5. View result with copy and preview options

### API Examples

#### cURL
```bash
# Create short URL
curl -X POST http://localhost:8398/api/short \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "custom_id": "example"}'

# Bulk creation
curl -X POST http://localhost:8398/api/urls/bulk \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://site1.com", "https://site2.com"]}'
```

#### Python
```python
import requests

# Create short URL
response = requests.post('http://localhost:8398/api/short', json={
    'url': 'https://www.python.org/',
    'custom_id': 'python',
    'title': 'Python Official'
})
data = response.json()
print(f"Short link: {data['short_link']}")
```

---

## 🧪 Development

### Test Suite
The application includes a comprehensive test suite:

```bash
# Run all tests
python run.py test

# Run specific test file
python -m pytest tests/unit/test_url_shortener.py -v
```

### Development Setup
1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd Url_Shortner_python
   ```

2. **Setup virtual environment**
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or venv\Scripts\activate  # Windows
   
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or
   uv add flask validators click
   ```

4. **Run tests**
   ```bash
   python run.py test
   ```

### Package Installation

#### Development Installation
```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

#### Production Installation
```bash
# Install package
pip install url-shortener-v2

# Use CLI commands
url-shortener run --port 5000
```

---

## 🏭 Configuration

### Environment Variables

```bash
# Database
DATABASE_PATH=url_shortener_v2.db

# Security
SECRET_KEY=your-secret-key
ADMIN_KEY=your-admin-key

# URLs
BASE_URL=https://your-domain.com
DEFAULT_EXPIRY_DAYS=30

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_DEFAULT_REQUESTS=30
RATE_LIMIT_BULK_REQUESTS=10

# Logging
LOG_LEVEL=INFO
LOG_FILE=url_shortener_v2.log
```

### Configuration Files

#### Development
```python
# Default configuration
DATABASE_PATH=url_shortener_v2.db
BASE_URL=http://localhost:8398
DEBUG=True
RATE_LIMIT_ENABLED=True
```

#### Production
```python
# Production configuration
SECRET_KEY=os.environ.get('SECRET_KEY')
BASE_URL=https://your-domain.com
DEBUG=False
RATE_LIMIT_ENABLED=True
RATE_LIMIT_DEFAULT_REQUESTS=20
```

---

## 📈 Features

### ✨ Core Features
- 🔗 **Smart URL Shortening** - Auto-generate or custom short URLs
- 📊 **Real-time Analytics** - Click tracking, browser analysis, referrer tracking
- ⚡ **Bulk Operations** - Shorten multiple URLs simultaneously
- 🛡️ **Rate Limiting** - Built-in request throttling
- 🎯 **Custom Metadata** - Support for titles, descriptions, and expiry
- 🔄 **Auto-cleanup** - Automatic expired URL management

### 🏗️ Technical Features
- 🏭 **Application Factory** - Flask factory pattern for scalability
- 📦 **Python Package** - Professional package structure
- 🔧 **CLI Tools** - Comprehensive management commands
- 🧪 **Test Suite** - Unit tests with pytest
- 📋 **Configuration** - Environment-based configuration
- 📝 **Documentation** - Comprehensive API documentation
- 🎨 **Modern UI** - Responsive web interface

### 🔒 Security Features
- **URL Validation** - Strict URL format and safety checking
- **Rate Limiting** - Per-IP request throttling
- **Input Sanitization** - XSS and injection prevention
- **Secure Headers** - Security-focused HTTP headers
- **Admin Protection** - Protected admin endpoints

---

## 🚀 Deployment

### Production Deployment

#### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8398
CMD ["python", "run.py", "run", "--config", "production"]
```

#### Using SystemD
```ini
[Unit]
Description=URL Shortener v2.0
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/url-shortener
ExecStart=/opt/url-shortener/venv/bin/python run.py run --config production
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Environment Setup
```bash
# Production environment
export FLASK_ENV=production
export DATABASE_PATH=/var/lib/url-shortener/url_shortener_v2.db
export BASE_URL=https://your-domain.com
export SECRET_KEY=your-production-secret-key

# Run with production config
python run.py run --config production
```

---

## 🛠️ Troubleshooting

### Common Issues

#### Database Issues
```bash
# Reset database
rm url_shortener_v2.db
python run.py init-db

# Check database
python run.py cleanup-expired
```

#### Permission Issues
```bash
# Fix permissions
chmod +x run.py
chmod 664 *.db *.log
```

#### Port Conflicts
```bash
# Use different port
python run.py run --port 8399
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python run.py run --debug
```

### Health Checks
```bash
# Check application health
curl http://localhost:8398/health

# Check API version
curl http://localhost:8398/api/version

# Test database
python run.py init-db
```

---

## 📦 Package Information

### Installation Methods

#### From PyPI (when published)
```bash
pip install url-shortener-v2
```

#### From Source
```bash
git clone <repository>
cd Url_Shortner_python
pip install -e .
```

### CLI Commands (when installed)
```bash
# Available commands
url-shortener run
url-shortener test
url-shortener init-db
url-shortener cleanup-expired
```

---

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run test suite: `python run.py test`
5. Submit pull request

### Code Standards
- **Python**: Follow PEP 8
- **Testing**: Add tests for new features
- **Documentation**: Update README and docstrings
- **Architecture**: Maintain separation of concerns

### Pull Request Guidelines
- Include comprehensive tests
- Update documentation
- Follow existing code style
- Add changelog entry

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
- ⭐ **Star** this repository
- 🐛 **Report bugs** via GitHub Issues
- 💡 **Suggest features** via GitHub Discussions
- 🤝 **Contribute** by submitting pull requests

---

<div align="center">

**🏗️ Professional Python Package • 🚀 Enterprise Features • 🛠️ CLI Management**

**Made with ❤️ using Python, Flask, and SQLite**

[⬆ Back to Top](#-url-shortener-v20---professional-python-package)

**🎯 URL Shortener v2.0 - Now as a Professional Python Package!**

</div>
