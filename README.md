# 🚀 Beautiful URL Shortener

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**A modern, feature-rich URL shortening service built with Python Flask**

[Features](#-features) • [Getting Started](#-getting-started) • [API Documentation](#-api-documentation) • [Examples](#-examples)

</div>

---

## ✨ Features

### Core Functionality
- 🔗 **URL Shortening** - Transform long URLs into concise, shareable links
- 🎯 **Custom IDs** - Create memorable short URLs with personalized identifiers
- ⏰ **Auto Expiry** - URLs automatically expire after 30 days
- 🔄 **Seamless Redirects** - Instant redirection to original URLs
- 📊 **Data Persistence** - JSON-based storage system
- 🌐 **Web Interface** - Clean, responsive web UI

### Technical Highlights
- ⚡ **Fast & Lightweight** - Built with Flask micro-framework
- 🔒 **Secure** - Input validation and error handling
- 🛠️ **RESTful API** - Full API support for automation
- 📱 **Responsive Design** - Works on all devices
- 🔍 **Error Handling** - Comprehensive error management

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/GrandmaEJ/api.git
   cd simple-url-shortener
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python index.py
   ```

4. **Access the service**
   - Web Interface: `http://localhost:8398`
   - API Base URL: `http://localhost:8398`

---

## 📖 API Documentation

### Base Configuration
- **Host URL**: `https://api-grandma-phpu.onrender.com/`
- **Port**: `8398`
- **Content-Type**: `application/json`

### Endpoints

#### 1. Create Short URL (POST)
Create a new shortened URL using JSON payload.

**Endpoint**: `POST /short`

**Request Body**:
```json
{
    "api": "your_api_key",
    "url": "https://example.com/very/long/url",
    "Alice": "custom_id" // optional
}
```

**Response**:
```json
{
    "status": 200,
    "short_link": "https://example.com/abc123",
    "id": "abc123",
    "redirect_link": "https://example.com/very/long/url",
    "making_date_time": "2025-10-30 06:32:54",
    "expired_time": "2025-11-29 06:32:54"
}
```

#### 2. Create Short URL (GET)
Create a short URL using query parameters.

**Endpoint**: `GET /short/api=<api_key>&url=<url>&Alice=<custom_id>`

**Example**:
```
GET /short/api=api1&url=https://example.com&Alice=mycustom
```

**Response**: Same as POST method

#### 3. Redirect to Original URL
Redirect users from short URL to original long URL.

**Endpoint**: `GET /<short_id>`

**Example**: `GET /abc123` → redirects to `https://example.com/very/long/url`

---

## 💡 Examples

### Using the Web Interface
1. Navigate to `http://localhost:8398`
2. Enter your long URL in the input field
3. Optionally specify a custom ID
4. Click "Shorten" to generate your short link

### Using cURL (POST)
```bash
curl -X POST http://localhost:8398/short \
  -H "Content-Type: application/json" \
  -d '{
    "api": "api1",
    "url": "https://github.com/python/cpython",
    "Alice": "pyrepo"
  }'
```

### Using JavaScript Fetch
```javascript
const response = await fetch('http://localhost:8398/short', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        api: 'api1',
        url: 'https://example.com/very/long/page',
        Alice: 'example'
    })
});

const result = await response.json();
console.log(result.short_link);
```

### Using Python Requests
```python
import requests

response = requests.post('http://localhost:8398/short', json={
    'api': 'api1',
    'url': 'https://www.python.org/',
    'Alice': 'pythonsite'
})

data = response.json()
print(f"Short link: {data['short_link']}")
```

---

## 🏗️ Project Structure

```
Url_Shortner_python/
├── 📄 index.py              # Main Flask application
├── 📄 us.py                 # Core URL shortening logic
├── 📄 utils.py              # Utility functions
├── 📄 requirements.txt      # Python dependencies
├── 📄 data.json            # URL storage (auto-generated)
├── 📄 log.txt              # Error logs (auto-generated)
├── 📁 templates/
│   └── 📄 index.html       # Web interface template
├── 📁 static/
│   ├── 📁 css/
│   │   └── 📄 styles.css   # Web styling
│   └── 📁 js/
│       └── 📄 main.js      # Frontend JavaScript
└── 📄 README.md            # This file
```

---

## ⚙️ Configuration

### Environment Variables
- **Host Link**: Modify `host_link` in `us.py` to change the base URL
- **Port**: Change `port` in `index.py` to use a different port
- **Expiry Time**: Adjust the 30-day expiry in `us.py` as needed

### Customization Options
- **Styling**: Edit `static/css/styles.css` for custom themes
- **UI**: Modify `templates/index.html` for interface changes
- **API Key**: Update API key validation in `us.py`

---

## 🔧 Technical Details

### URL Generation Algorithm
- **Default**: MD5 hash of the original URL (first 6 characters)
- **Custom**: User-provided identifier (validated for uniqueness)
- **Format**: Alphanumeric characters only

### Data Storage
- **Format**: JSON file (`data.json`)
- **Structure**: Dictionary with URL mappings
- **Fields**: `original_url`, `creation_time`, `expiry_time`, `Alice`

### Error Handling
- Missing parameters → HTTP 505
- Expired URLs → HTTP 404
- Custom ID conflicts → HTTP 505
- Invalid URLs → HTTP 404

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support & Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Change port in index.py
app.run(debug=True, host='0.0.0.0', port=8399)
```

**Permission Errors**
```bash
# Ensure write permissions for data.json and log.txt
chmod 664 data.json log.txt
```

**API Returns 505 Error**
- Check if `api` and `url` parameters are provided
- Verify request format (JSON vs form data)

---

<div align="center">

**Made with ❤️ using Python and Flask**

[⬆ Back to Top](#-beautiful-url-shortener)

</div>
