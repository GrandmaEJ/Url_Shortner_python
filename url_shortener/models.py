import sqlite3
import hashlib
import datetime
import json
import validators
from typing import Optional, Dict, List, Any


class URLModel:
    """Database model for URL shortening operations"""
    
    def __init__(self, db_path: str = "url_shortener_v2.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create URLs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
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
            )
        ''')
        
        # Create click_analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS click_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_id TEXT NOT NULL,
                click_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_agent TEXT,
                referrer TEXT,
                ip_address TEXT,
                FOREIGN KEY (short_id) REFERENCES urls (short_id)
            )
        ''')
        
        # Create rate_limit table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rate_limit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                request_count INTEGER DEFAULT 1,
                window_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_short_id ON urls(short_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_creation_time ON urls(creation_time)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_click_analytics_short_id ON click_analytics(short_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_rate_limit_ip ON rate_limit(ip_address, endpoint)')
        
        conn.commit()
        conn.close()
    
    def create_short_url(self, original_url: str, custom_id: Optional[str] = None, 
                        api_key: str = "default", title: str = "", description: str = "",
                        created_by_ip: str = "", expiry_days: int = 30) -> Dict[str, Any]:
        """Create a new shortened URL"""
        # Validate URL
        if not validators.url(original_url):
            raise ValueError("Invalid URL format")
        
        # Generate short_id if not provided
        if custom_id:
            short_id = custom_id
        else:
            short_id = self.generate_short_id(original_url)
        
        # Check if short_id already exists
        if self.get_url_by_short_id(short_id):
            raise ValueError("Short ID already exists")
        
        # Calculate expiry time
        expiry_time = datetime.datetime.now() + datetime.timedelta(days=expiry_days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO urls (short_id, original_url, custom_id, expiry_time, 
                            api_key, title, description, created_by_ip)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (short_id, original_url, custom_id, expiry_time.isoformat(), 
              api_key, title, description, created_by_ip))
        
        url_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return self.get_url_by_id(url_id)
    
    def get_url_by_short_id(self, short_id: str) -> Optional[Dict[str, Any]]:
        """Get URL by short ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, short_id, original_url, custom_id, creation_time, 
                   expiry_time, click_count, is_active, api_key, title, description
            FROM urls WHERE short_id = ? AND is_active = 1
        ''', (short_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'short_id': result[1],
                'original_url': result[2],
                'custom_id': result[3],
                'creation_time': result[4],
                'expiry_time': result[5],
                'click_count': result[6],
                'is_active': result[7],
                'api_key': result[8],
                'title': result[9],
                'description': result[10]
            }
        return None
    
    def get_url_by_id(self, url_id: int) -> Optional[Dict[str, Any]]:
        """Get URL by database ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, short_id, original_url, custom_id, creation_time, 
                   expiry_time, click_count, is_active, api_key, title, description
            FROM urls WHERE id = ? AND is_active = 1
        ''', (url_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'short_id': result[1],
                'original_url': result[2],
                'custom_id': result[3],
                'creation_time': result[4],
                'expiry_time': result[5],
                'click_count': result[6],
                'is_active': result[7],
                'api_key': result[8],
                'title': result[9],
                'description': result[10]
            }
        return None
    
    def increment_click_count(self, short_id: str, user_agent: str = "", 
                            referrer: str = "", ip_address: str = ""):
        """Increment click count and log analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update click count
        cursor.execute('''
            UPDATE urls SET click_count = click_count + 1 
            WHERE short_id = ? AND is_active = 1
        ''', (short_id,))
        
        # Log analytics
        cursor.execute('''
            INSERT INTO click_analytics (short_id, user_agent, referrer, ip_address)
            VALUES (?, ?, ?, ?)
        ''', (short_id, user_agent, referrer, ip_address))
        
        conn.commit()
        conn.close()
    
    def get_analytics(self, short_id: str) -> Dict[str, Any]:
        """Get analytics for a short URL"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get basic URL info
        url_info = self.get_url_by_short_id(short_id)
        if not url_info:
            return {}
        
        # Get click analytics
        cursor.execute('''
            SELECT DATE(click_time) as date, COUNT(*) as clicks
            FROM click_analytics 
            WHERE short_id = ? 
            GROUP BY DATE(click_time)
            ORDER BY date DESC
            LIMIT 30
        ''', (short_id,))
        
        daily_clicks = cursor.fetchall()
        
        cursor.execute('''
            SELECT user_agent, COUNT(*) as clicks
            FROM click_analytics 
            WHERE short_id = ?
            GROUP BY user_agent
            ORDER BY clicks DESC
            LIMIT 10
        ''', (short_id,))
        
        user_agents = cursor.fetchall()
        
        cursor.execute('''
            SELECT referrer, COUNT(*) as clicks
            FROM click_analytics 
            WHERE short_id = ? AND referrer != ''
            GROUP BY referrer
            ORDER BY clicks DESC
            LIMIT 10
        ''', (short_id,))
        
        referrers = cursor.fetchall()
        
        conn.close()
        
        return {
            'url_info': url_info,
            'daily_clicks': [{'date': row[0], 'clicks': row[1]} for row in daily_clicks],
            'user_agents': [{'user_agent': row[0], 'clicks': row[1]} for row in user_agents],
            'referrers': [{'referrer': row[0], 'clicks': row[1]} for row in referrers]
        }
    
    def bulk_create_urls(self, urls_data: List[Dict[str, Any]], api_key: str = "default") -> List[Dict[str, Any]]:
        """Create multiple shortened URLs at once"""
        results = []
        for url_data in urls_data:
            try:
                result = self.create_short_url(
                    original_url=url_data['url'],
                    custom_id=url_data.get('custom_id'),
                    api_key=api_key,
                    title=url_data.get('title', ''),
                    description=url_data.get('description', ''),
                    created_by_ip=url_data.get('created_by_ip', ''),
                    expiry_days=url_data.get('expiry_days', 30)
                )
                results.append(result)
            except Exception as e:
                results.append({'error': str(e), 'url': url_data['url']})
        
        return results
    
    def generate_short_id(self, url: str) -> str:
        """Generate a unique short ID"""
        # Create hash from URL
        hash_obj = hashlib.md5(url.encode())
        base_id = hash_obj.hexdigest()[:6]
        
        # Ensure uniqueness
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        counter = 1
        while True:
            candidate_id = base_id + str(counter) if counter > 1 else base_id
            
            cursor.execute('SELECT 1 FROM urls WHERE short_id = ?', (candidate_id,))
            if not cursor.fetchone():
                break
            
            counter += 1
        
        conn.close()
        return candidate_id
    
    def cleanup_expired_urls(self) -> int:
        """Remove expired URLs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE urls SET is_active = 0 
            WHERE expiry_time < CURRENT_TIMESTAMP AND is_active = 1
        ''')
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def get_all_urls(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all active URLs with pagination"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, short_id, original_url, custom_id, creation_time, 
                   expiry_time, click_count, is_active, api_key, title, description
            FROM urls 
            WHERE is_active = 1
            ORDER BY creation_time DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'short_id': row[1],
                'original_url': row[2],
                'custom_id': row[3],
                'creation_time': row[4],
                'expiry_time': row[5],
                'click_count': row[6],
                'is_active': row[7],
                'api_key': row[8],
                'title': row[9],
                'description': row[10]
            })
        
        conn.close()
        return results


class RateLimitModel:
    """Database model for rate limiting operations"""
    
    def __init__(self, db_path: str = "url_shortener_v2.db"):
        self.db_path = db_path
    
    def is_rate_limited(self, ip_address: str, endpoint: str, max_requests: int = 60, 
                       window_minutes: int = 1) -> bool:
        """Check if IP is rate limited"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clean old entries
        window_start = datetime.datetime.now() - datetime.timedelta(minutes=window_minutes)
        cursor.execute('DELETE FROM rate_limit WHERE window_start < ?', (window_start.isoformat(),))
        
        # Check current requests
        cursor.execute('''
            SELECT SUM(request_count) 
            FROM rate_limit 
            WHERE ip_address = ? AND endpoint = ? AND window_start >= ?
        ''', (ip_address, endpoint, window_start.isoformat()))
        
        total_requests = cursor.fetchone()[0] or 0
        
        if total_requests >= max_requests:
            conn.close()
            return True
        
        # Increment or insert rate limit record
        cursor.execute('''
            INSERT INTO rate_limit (ip_address, endpoint, request_count, window_start)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(ip_address, endpoint) DO UPDATE SET 
            request_count = request_count + 1
        ''', (ip_address, endpoint, datetime.datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return False