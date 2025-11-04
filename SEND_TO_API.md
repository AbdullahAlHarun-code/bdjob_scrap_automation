# 📡 Sending BD Govt Jobs to API

## 🎯 Overview

The `bdgovtjob.py` scraper now **automatically sends data to your Django API** after scraping!

**Default API URL:** `http://127.0.0.1:8000/bdgovjob/send-data/`

---

## 🚀 Quick Start

### **Step 1: Start Django Server**

```bash
cd bdjob_api_restframework/django-n8n-api

# Run migrations (first time only)
python manage.py makemigrations bdgovjob
python manage.py migrate

# Start server
python manage.py runserver
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### **Step 2: Run Scraper**

```bash
# In another terminal
cd github_bdjob
python bdgovtjob.py
```

**The scraper will:**
1. ✅ Scrape 20 pages from bdgovtjob.net
2. ✅ Save to `bdgovtjob_data.csv`
3. ✅ Save to `bdgovtjob_data.json`
4. ✅ **Send all data to API automatically!**

---

## 📊 Expected Output

```
============================================================
🚀 BD GOVT JOB SCRAPER - STARTING
============================================================
Target: https://bdgovtjob.net/category/government-jobs-circular/
Max pages: 20
Method: Direct URL navigation
============================================================

📡 Loading page 1: https://bdgovtjob.net/category/government-jobs-circular/...
✅ Page 1 loaded!
...

============================================================
✅ SCRAPING COMPLETE!
Total pages scraped: 20
Total jobs collected: 200
============================================================

✅ CSV saved: C:\VSCode\N8n\github_bdjob\bdgovtjob_data.csv
   Rows: 200

✅ JSON saved: C:\VSCode\N8n\github_bdjob\bdgovtjob_data.json
   Records: 200

============================================================
🎉 SUCCESS! Data saved to:
   📄 bdgovtjob_data.csv
   📄 bdgovtjob_data.json
============================================================

============================================================
📡 Sending data to API...
   API URL: http://127.0.0.1:8000/bdgovjob/send-data/
   Jobs to send: 200
============================================================

✅ API Response Success!
   Created: 200 jobs
   Updated: 0 jobs
   Errors: 0

📊 SUMMARY:
   Total jobs: 200
   Jobs with vacancy info: 192
   Total vacancies: 3,847
   Jobs with deadline: 198

✅ Scraper finished!
```

---

## 🔧 Configuration

### **Change API URL**

```bash
# Use custom API URL
set API_URL=http://your-server.com/bdgovjob/send-data/
python bdgovtjob.py
```

### **Disable API Sending**

Edit `bdgovtjob.py` and comment out this line:

```python
# scraper.send_jobs_to_api(api_url)
```

### **Change Max Pages**

```bash
# Scrape only 5 pages
set MAX_PAGES=5
python bdgovtjob.py

# Scrape 50 pages
set MAX_PAGES=50
python bdgovtjob.py
```

---

## ✅ Verify Data in API

### **Method 1: Check Stats**

```bash
curl http://127.0.0.1:8000/bdgovjob/stats/
```

**Response:**
```json
{
  "total_jobs": 200,
  "today": 200,
  "this_week": 200,
  "this_month": 200,
  "with_vacancies": 192,
  "with_deadlines": 198,
  "last_updated": "2025-11-03T23:15:00Z"
}
```

### **Method 2: Get Today's Jobs**

```bash
curl http://127.0.0.1:8000/bdgovjob/get-data/today/
```

### **Method 3: Use Admin Panel**

1. Go to `http://127.0.0.1:8000/admin/`
2. Login with superuser
3. Click **Government Jobs**
4. See all scraped jobs!

---

## 🔄 How It Works

### **Deduplication by URL**

The API uses `job_url` as a unique identifier:

- **First run:** Creates 200 new jobs ✅
- **Second run (same jobs):** Updates existing 200 jobs ✅
- **No duplicates!** 🎯

### **Example:**

```
Run 1: Scrapes Job A, B, C → API creates 3 records
Run 2: Scrapes Job A, B, D → API updates A, B and creates D
Result: 4 total records (A, B, C, D) with latest data
```

---

## 🐛 Troubleshooting

### **Problem: "Cannot connect to API"**

**Cause:** Django server is not running.

**Solution:**
```bash
cd bdjob_api_restframework/django-n8n-api
python manage.py runserver
```

### **Problem: "Table doesn't exist"**

**Cause:** Migrations not run.

**Solution:**
```bash
cd bdjob_api_restframework/django-n8n-api
python manage.py makemigrations bdgovjob
python manage.py migrate
```

### **Problem: "API Error: HTTP 500"**

**Cause:** Server error, check Django console.

**Solution:**
1. Look at Django server terminal for error details
2. Common issue: Missing fields or wrong data format
3. Check `BDGOVJOB_API_DOCUMENTATION.md` for correct format

### **Problem: "API request timed out"**

**Cause:** Too many jobs to send at once.

**Solution:**
1. Use smaller `MAX_PAGES` value
2. Increase timeout in `bdgovtjob.py` (currently 60s)

### **Problem: Data sends but shows 0 created**

**Cause:** All jobs already exist (duplicates).

**Solution:**
- ✅ This is normal! Check `Updated: X jobs` instead
- The API updates existing records with latest data
- To force new records, change `job_url` or clear database

---

## 📈 Batch Processing

### **Send Existing JSON File**

If you already have `bdgovtjob_data.json`:

```python
import requests
import json

# Read the JSON file
with open('bdgovtjob_data.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

# Send to API
response = requests.post(
    'http://127.0.0.1:8000/bdgovjob/send-data/',
    json=jobs,
    headers={'Content-Type': 'application/json'}
)

print(response.json())
```

### **Send in Smaller Batches**

For very large datasets (>500 jobs):

```python
import requests
import json

with open('bdgovtjob_data.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

batch_size = 100
for i in range(0, len(jobs), batch_size):
    batch = jobs[i:i+batch_size]
    response = requests.post(
        'http://127.0.0.1:8000/bdgovjob/send-data/',
        json=batch
    )
    print(f"Batch {i//batch_size + 1}: {response.json()['total_created']} created")
```

---

## 🚀 Production Deployment

### **On DigitalOcean Droplet:**

```bash
# Set production API URL
export API_URL=http://your-server.com/bdgovjob/send-data/

# Run scraper
MAX_PAGES=20 python bdgovtjob.py
```

### **Automated with Cron:**

```bash
# Edit crontab
crontab -e

# Add this line (runs 3x daily at 3am, 9am, 3pm)
0 3,9,15 * * * cd /root/bdjob_scrap_automation && API_URL=http://your-server.com/bdgovjob/send-data/ MAX_PAGES=20 /root/venv/bin/python bdgovtjob.py >> /root/bdgovtjob_scraper.log 2>&1
```

---

## 📊 API Response Format

### **Success Response:**

```json
{
  "created": [
    {
      "id": 1,
      "job_title": "Planning Division Job Circular 2025",
      "job_url": "https://bdgovtjob.net/planning-division-job-circular/",
      "vacancies": "65",
      "deadline": "25 November 2025 at 5:00 PM",
      "posted_date": "3 November, 2025",
      "scraped_at": "2025-11-03T23:12:47Z",
      "created_at": "2025-11-03T23:15:00Z",
      "updated_at": "2025-11-03T23:15:00Z"
    }
  ],
  "updated": [],
  "skipped": [],
  "total_created": 1,
  "total_updated": 0,
  "total_errors": 0
}
```

### **Error Response:**

```json
{
  "created": [],
  "updated": [],
  "skipped": [],
  "total_created": 0,
  "total_updated": 0,
  "total_errors": 2,
  "errors": [
    {
      "item": {...},
      "errors": {
        "job_url": ["This field is required."]
      }
    }
  ]
}
```

---

## 🎯 Summary

✅ **Scraper automatically sends data to API**  
✅ **Default URL: `http://127.0.0.1:8000/bdgovjob/send-data/`**  
✅ **No duplicates (deduplication by job_url)**  
✅ **Updates existing records automatically**  
✅ **Detailed error reporting**  
✅ **Works with cron jobs for automation**  

---

**Your scraper is now integrated with the API!** 🎉

Just run:
1. `python manage.py runserver` (Django)
2. `python bdgovtjob.py` (Scraper)

Done! 🚀

