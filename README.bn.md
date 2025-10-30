# 🚀 URL Shortener v2.0 - পেশাদার পাইথন প্যাকেজ

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-ডেটাবেস-green?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/লাইসেন্স-MIT-green.svg)
![Version](https://img.shields.io/badge/সংস্করণ-2.0-success.svg)

**বিশ্লেষণ, বাল্ক অপারেশন এবং এন্টারপ্রাইজ ফিচার সহ পেশাদার URL সংক্ষিপ্তকরণ পরিষেবা**

[🏗️ আর্কিটেকচার](#-আর্কিটেকচার) • [🚀 দ্রুত শুরু](#-দ্রুত-শুরু) • [🛠️ CLI কমান্ডস](#-cli-কমান্ডস) • [📖 API ডকুমেন্টেশন](#-api-ডকুমেন্টেশন)

</div>

---

## 🏗️ আর্কিটেকচার

### প্যাকেজ স্ট্রাকচার
কোডবেস পেশাদার পাইথন প্যাকেজ স্ট্রাকচারে পুনর্গঠিত হয়েছে:

```
Url_Shortner_python/
├── 📁 url_shortener/              # মূল পাইথন প্যাকেজ
│   ├── 📄 app.py                 # ফ্লাস্ক অ্যাপ্লিকেশন ফ্যাক্টরি
│   ├── 📄 config.py              # কনফিগারেশন ম্যানেজমেন্ট
│   ├── 📄 models.py              # ডেটাবেস মডেল ও অপারেশন
│   ├── 📄 services.py            # ব্যবসায়িক লজিক ও পরিষেবা
│   ├── 📄 routes.py              # API রুট এন্ডপয়েন্ট
│   ├── 📄 utils.py               # ইউটিলিটি ফাংশন
│   ├── 📁 templates/             # জিনজা২ টেমপ্লেট
│   └── 📁 static/                # স্ট্যাটিক ফাইল (CSS, JS)
├── 📁 tests/                     # টেস্ট সুইট
├── 📄 run.py                     # CLI এন্ট্রি পয়েন্ট
├── 📄 requirements.txt           # পাইথন নির্ভরতা
└── 📄 README.bn.md               # এই ফাইল
```

---

## 🚀 দ্রুত শুরু

### ইনস্টলেশন

1. **ক্লোন করুন এবং সেটআপ করুন**
   ```bash
   git clone https://github.com/GrandmaEJ/api.git
   cd Url_Shortner_python
   ```

2. **নির্ভরতা ইনস্টল করুন**
   ```bash
   pip install -r requirements.txt
   ```

3. **ডেটাবেস ইনিশিয়ালাইজ করুন**
   ```bash
   python run.py init-db
   ```

4. **সার্ভার চালু করুন**
   ```bash
   python run.py run
   ```

5. **অ্যাপ্লিকেশন অ্যাক্সেস করুন**
   - 🌐 **ওয়েব ইন্টারফেস**: `http://localhost:8398`
   - 🔗 **API বেস**: `http://localhost:8398/api`
   - 📊 **হেলথ চেক**: `http://localhost:8398/health`

---

## 🛠️ CLI কমান্ডস

### সার্ভার ম্যানেজমেন্ট
```bash
# ডেভেলপমেন্ট সার্ভার চালু করুন
python run.py run

# কাস্টম অপশন সহ চালু করুন
python run.py run --host 0.0.0.0 --port 5000 --debug

# নির্দিষ্ট কনফিগারেশন ব্যবহার করুন
python run.py run --config production
```

### ডেটাবেস ম্যানেজমেন্ট
```bash
# ডেটাবেস ইনিশিয়ালাইজ করুন
python run.py init-db

# মেয়াদোত্তীর্ণ URL পরিষ্কার করুন
python run.py cleanup-expired
```

### টেস্টিং
```bash
# টেস্ট সুইট চালু করুন
python run.py test
```

---

## 📖 API ডকুমেন্টেশন

### বেস কনফিগারেশন
- **বেস URL**: `http://localhost:8398`
- **API সংস্করণ**: `v2.0`
- **Content-Type**: `application/json`

### 🔗 কোর এন্ডপয়েন্টস

#### 1. সংক্ষিপ্ত URL তৈরি করুন (POST)
```bash
POST /api/short
Content-Type: application/json

{
    "url": "https://example.com/very/long/url",
    "custom_id": "mycustom",        # ঐচ্ছিক
    "title": "My Website",          # ঐচ্ছিক
    "description": "Main website",  # ঐচ্ছিক
    "expiry_days": 30               # ঐচ্ছিক (ডিফল্ট: 30)
}
```

#### 2. বাল্ক URL তৈরি করুন
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

#### 3. URL বিশ্লেষণ
```bash
GET /api/urls/<short_id>/analytics
```

#### 4. সকল URL তালিকা
```bash
GET /api/urls?limit=50&offset=0
```

#### 5. পুনর্নির্দেশ
```bash
GET /<short_id>  # মূল URL-এ পুনর্নির্দেশিত করে
```

### 🔍 হেলথ ও স্ট্যাটাস এন্ডপয়েন্টস

#### হেলথ চেক
```bash
GET /health
Response: {"status": "healthy", "version": "2.0.0"}
```

#### API সংস্করণ
```bash
GET /api/version
Response: {"version": "2.0.0", "status": "active"}
```

---

## 🎯 উদাহরণ

### ওয়েব ইন্টারফেস ব্যবহার
1. `http://localhost:8398`-এ যান
2. আপনার দীর্ঘ URL লিখুন
3. ঐচ্ছিকভাবে কাস্টম ID, শিরোনাম এবং বিবরণ যোগ করুন
4. "Shorten URL" ক্লিক করুন
5. কপি এবং প্রিভিউ অপশন সহ ফলাফল দেখুন

### API উদাহরণ

#### cURL
```bash
# সংক্ষিপ্ত URL তৈরি করুন
curl -X POST http://localhost:8398/api/short \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "custom_id": "example"}'

# বাল্ক তৈরি করুন
curl -X POST http://localhost:8398/api/urls/bulk \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://site1.com", "https://site2.com"]}'
```

#### Python
```python
import requests

# সংক্ষিপ্ত URL তৈরি করুন
response = requests.post('http://localhost:8398/api/short', json={
    'url': 'https://www.python.org/',
    'custom_id': 'python',
    'title': 'Python Official'
})
data = response.json()
print(f"Short link: {data['short_link']}")
```

---

## 🧪 ডেভেলপমেন্ট

### টেস্ট সুইট
অ্যাপ্লিকেশনে একটি বিস্তৃত টেস্ট সুইট অন্তর্ভুক্ত:

```bash
# সকল টেস্ট চালু করুন
python run.py test

# নির্দিষ্ট টেস্ট ফাইল চালু করুন
python -m pytest tests/unit/test_url_shortener.py -v
```

### ডেভেলপমেন্ট সেটআপ
1. **রিপোজিটরি ক্লোন করুন**
   ```bash
   git clone <repository-url>
   cd Url_Shortner_python
   ```

2. **ভার্চুয়াল এনভায়রনমেন্ট সেটআপ করুন**
   ```bash
   # venv ব্যবহার করে
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # অথবা venv\Scripts\activate  # Windows
   
   # uv ব্যবহার করে (প্রস্তাবিত)
   uv venv
   source .venv/bin/activate
   ```

3. **নির্ভরতা ইনস্টল করুন**
   ```bash
   pip install -r requirements.txt
   # অথবা
   uv add flask validators click
   ```

4. **টেস্ট চালু করুন**
   ```bash
   python run.py test
   ```

---

## 📈 ফিচারসমূহ

### ✨ কোর ফিচারস
- 🔗 **স্মার্ট URL সংক্ষিপ্তকরণ** - অটো-জেনারেট বা কাস্টম সংক্ষিপ্ত URL
- 📊 **রিয়েল-টাইম বিশ্লেষণ** - ক্লিক ট্র্যাকিং, ব্রাউজার বিশ্লেষণ, রেফারার ট্র্যাকিং
- ⚡ **বাল্ক অপারেশন** - একসাথে একাধিক URL সংক্ষিপ্তকরণ
- 🛡️ **রেট লিমিটিং** - বিল্ট-ইন রিকোয়েস্ট থ্রটলিং
- 🎯 **কাস্টম মেটাডাটা** - শিরোনাম, বিবরণ এবং মেয়াদ শেষের জন্য সহায়তা
- 🔄 **অটো-ক্লিনআপ** - স্বয়ংক্রিয় মেয়াদোত্তীর্ণ URL ম্যানেজমেন্ট

### 🏗️ প্রযুক্তিগত ফিচারস
- 🏭 **অ্যাপ্লিকেশন ফ্যাক্টরি** - স্কেলেবিলিটির জন্য ফ্লাস্ক ফ্যাক্টরি প্যাটার্ন
- 📦 **পাইথন প্যাকেজ** - পেশাদার প্যাকেজ স্ট্রাকচার
- 🔧 **CLI টুলস** - বিস্তৃত ম্যানেজমেন্ট কমান্ড
- 🧪 **টেস্ট সুইট** - pytest সহ ইউনিট টেস্ট
- 📋 **কনফিগারেশন** - এনভায়রনমেন্ট-ভিত্তিক কনফিগারেশন
- 📝 **ডকুমেন্টেশন** - বিস্তৃত API ডকুমেন্টেশন
- 🎨 **আধুনিক UI** - রেসপন্সিভ ওয়েব ইন্টারফেস

---

## 🚀 ডিপ্লয়মেন্ট

### প্রোডাকশন ডিপ্লয়মেন্ট

#### Docker ব্যবহার করে
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8398
CMD ["python", "run.py", "run", "--config", "production"]
```

#### SystemD ব্যবহার করে
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

#### এনভায়রনমেন্ট সেটআপ
```bash
# প্রোডাকশন এনভায়রনমেন্ট
export FLASK_ENV=production
export DATABASE_PATH=/var/lib/url-shortener/url_shortener_v2.db
export BASE_URL=https://your-domain.com
export SECRET_KEY=your-production-secret-key

# প্রোডাকশন কনফিগ সহ চালু করুন
python run.py run --config production
```

---

## 🛠️ সমস্যা সমাধান

### সাধারণ সমস্যাসমূহ

#### ডেটাবেস সমস্যাসমূহ
```bash
# ডেটাবেস রিসেট করুন
rm url_shortener_v2.db
python run.py init-db

# ডেটাবেস পরীক্ষা করুন
python run.py cleanup-expired
```

#### অনুমতির সমস্যাসমূহ
```bash
# অনুমতি ঠিক করুন
chmod +x run.py
chmod 664 *.db *.log
```

#### পোর্ট সংঘর্ষ
```bash
# ভিন্ন পোর্ট ব্যবহার করুন
python run.py run --port 8399
```

### ডিবাগ মোড
```bash
# ডিবাগ লগিং সক্ষম করুন
export LOG_LEVEL=DEBUG
python run.py run --debug
```

### হেলথ চেকসমূহ
```bash
# অ্যাপ্লিকেশন হেলথ পরীক্ষা করুন
curl http://localhost:8398/health

# API সংস্করণ পরীক্ষা করুন
curl http://localhost:8398/api/version

# ডেটাবেস টেস্ট করুন
python run.py init-db
```

---

## 🤝 অবদান

### ডেভেলপমেন্ট ওয়ার্কফ্লো
1. রিপোজিটরি ফর্ক করুন
2. ফিচার ব্রাঞ্চ তৈরি করুন: `git checkout -b feature-name`
3. পরিবর্তন করুন এবং টেস্ট যোগ করুন
4. টেস্ট সুইট চালু করুন: `python run.py test`
5. পুল রিকোয়েস্ট জমা দিন

### কোড স্ট্যান্ডার্ড
- **পাইথন**: PEP 8 অনুসরণ করুন
- **টেস্টিং**: নতুন ফিচারের জন্য টেস্ট যোগ করুন
- **ডকুমেন্টেশন**: README এবং ডকস্ট্রিং আপডেট করুন
- **আর্কিটেকচার**: উদ্বেগের পৃথকীকরণ বজায় রাখুন

---

## 📄 লাইসেন্স

এই প্রজেক্ট MIT লাইসেন্সের অধীনে লাইসেন্সপ্রাপ্ত - বিস্তারিত জানার জন্য [LICENSE](LICENSE) ফাইল দেখুন।

---

## 🆘 সহায়তা

### সাহায্য পাওয়া
- 📧 **ইস্যুসমূহ**: [GitHub Issues](https://github.com/GrandmaEJ/api/issues)
- 💬 **আলোচনাসমূহ**: [GitHub Discussions](https://github.com/GrandmaEJ/api/discussions)
- 📖 **উইকি**: [প্রজেক্ট উইকি](https://github.com/GrandmaEJ/api/wiki)

### কমিউনিটি
- ⭐ **স্টার** এই রিপোজিটরি
- 🐛 **বাগ রিপোর্ট** GitHub Issues এর মাধ্যমে
- 💡 **ফিচার সাজেশন** GitHub Discussions এর মাধ্যমে
- 🤝 **অবদান** পুল রিকোয়েস্ট জমা দিয়ে

---

<div align="center">

**🏗️ পেশাদার পাইথন প্যাকেজ • 🚀 এন্টারপ্রাইজ ফিচারস • 🛠️ CLI ম্যানেজমেন্ট**

**❤️ দিয়ে তৈরি পাইথন, ফ্লাস্ক এবং SQLite ব্যবহার করে**

[⬆ উপরে ফিরে যান](#-url-shortener-v20---পেশাদার-পাইথন-প্যাকেজ)

**🎯 URL Shortener v2.0 - এখন একটি পেশাদার পাইথন প্যাকেজ হিসাবে!**

</div>