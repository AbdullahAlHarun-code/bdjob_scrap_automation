# 🪟 Windows Setup Guide - BD Govt Job Scraper

## ⚡ Quick Install (Recommended)

**Step 1:** Open **CMD** (Command Prompt) - NOT PowerShell  
Press `Win + R`, type `cmd`, press Enter

**Step 2:** Navigate to project folder
```cmd
cd C:\VSCode\N8n\github_bdjob
```

**Step 3:** Run the installer
```cmd
install_dependencies.bat
```

This will automatically install all required packages and test your setup!

---

## 🔧 Manual Install (If batch file doesn't work)

Open **CMD** and run these commands one by one:

```cmd
cd C:\VSCode\N8n\github_bdjob

python -m pip install --upgrade pip
python -m pip install selenium
python -m pip install pandas
python -m pip install webdriver-manager
python -m pip install beautifulsoup4
python -m pip install lxml

python test_scraper.py
```

---

## ✅ Test Your Setup

```cmd
python test_scraper.py
```

**Expected output:**
```
============================================================
Testing imports for bdgovtjob scraper...
============================================================
1. Importing selenium... ✓
2. Importing pandas... ✓
3. Importing webdriver_manager... ✓
4. Importing beautifulsoup4... ✓

============================================================
✅ ALL DEPENDENCIES INSTALLED!

You can now run the scraper:
  python bdgovtjob.py
============================================================
```

---

## 🚀 Run the Scraper

### Scrape 1 page (quick test):
```cmd
set MAX_PAGES=1
python bdgovtjob.py
```

### Scrape 20 pages (default - recommended):
```cmd
python bdgovtjob.py
```

This will scrape:
- Page 1: https://bdgovtjob.net/category/government-jobs-circular/
- Page 2: https://bdgovtjob.net/category/government-jobs-circular/page/2/
- Page 3: https://bdgovtjob.net/category/government-jobs-circular/page/3/
- ...
- Page 20: https://bdgovtjob.net/category/government-jobs-circular/page/20/

**Total: ~200 jobs (10 jobs per page × 20 pages)**

### Scrape more pages (e.g. 50 pages):
```cmd
set MAX_PAGES=50
python bdgovtjob.py
```

---

## 📁 Output Files

After running, you'll get:
- ✅ `bdgovtjob_data.csv` - CSV format
- ✅ `bdgovtjob_data.json` - JSON format
- 📝 `debug_bdgovtjob_page.html` - Debug file (shows what Selenium sees)

---

## ❌ Troubleshooting

### Problem: "No module named 'pandas'"

**Solution 1:** Use `py` launcher instead of `python`
```cmd
py -m pip install pandas selenium webdriver-manager beautifulsoup4
py bdgovtjob.py
```

**Solution 2:** Install Python from python.org (not Windows Store)
1. Go to https://python.org/downloads
2. Download and install Python 3.11+
3. During install, check "Add Python to PATH"
4. Restart CMD and try again

### Problem: PowerShell doesn't work

**Solution:** Use CMD instead!
- PowerShell has different syntax that causes issues
- CMD is more reliable for Python scripts

### Problem: Job titles are empty

**Solution:** Already fixed! The scraper now uses:
- ✅ Multiple extraction methods (`.text`, `innerText`, `textContent`)
- ✅ Fallback to `aria-label` and `title` attributes
- ✅ Debug HTML save to troubleshoot

Just run the scraper and it should extract job titles properly now!

---

## 🎯 What's New

### Improved Text Extraction ✨

The scraper now uses **robust multi-method extraction**:

```python
def extract_link_text(el):
    # 1) Normal Selenium text (visible text)
    t = el.text.strip()
    if t: return t
    
    # 2) DOM text properties
    for attr in ("innerText", "textContent"):
        t = (el.get_attribute(attr) or "").strip()
        if t: return " ".join(t.split())  # normalize whitespace
    
    # 3) Useful attributes some themes set
    for attr in ("aria-label", "title"):
        t = (el.get_attribute(attr) or "").strip()
        if t: return t
    
    return ""
```

This ensures **job titles, vacancies, and deadlines** are extracted correctly!

---

## 📊 Expected Results

**Console Output:**
```
============================================================
🚀 BD GOVT JOB SCRAPER - STARTING
============================================================
Target: https://bdgovtjob.net/category/government-jobs-circular/
Max pages: 10
============================================================

📡 Loading https://bdgovtjob.net/category/government-jobs-circular/...
✅ Page loaded successfully!
📝 DEBUG: Saved page HTML to 'debug_bdgovtjob_page.html'

============================================================
📄 Scraping Page 1
============================================================
Found 10 job articles on page 1
  ✓ [1/10] Planning Division Job Circular 2025... | V:65 | D:25 November...
  ✓ [2/10] Bangladesh Bank Job Circular... | V:125 | D:30 November...
  ...
✅ Page 1 complete: 10 jobs extracted

============================================================
✅ SCRAPING COMPLETE!
Total pages scraped: 10
Total jobs collected: 100
============================================================

✅ CSV saved: C:\VSCode\N8n\github_bdjob\bdgovtjob_data.csv
   Rows: 100
✅ JSON saved: C:\VSCode\N8n\github_bdjob\bdgovtjob_data.json
   Records: 100

📊 SUMMARY:
   Total jobs: 100
   Jobs with vacancy info: 95
   Total vacancies: 1,850
   Jobs with deadline: 98

✅ Scraper finished!
```

---

## 🆘 Need Help?

1. Run `test_scraper.py` first to check dependencies
2. Check `debug_bdgovtjob_page.html` to see what Selenium sees
3. Make sure you're using **CMD** not PowerShell
4. Install Python from python.org if Windows Store version has issues

---

## 🎯 Next Steps

Once the scraper works locally:

### Deploy to DigitalOcean Droplet:

```bash
# Push to GitHub
git add .
git commit -m "Fixed bdgovtjob scraper with improved text extraction"
git push origin main

# On Droplet
cd /root/bdjob_scrap_automation
git pull origin main

# Install dependencies (if needed)
/root/venv/bin/pip install pandas beautifulsoup4 lxml

# Test
MAX_PAGES=2 /root/venv/bin/python bdgovtjob.py

# Add to cron (run 3x daily at 3am, 9am, 3pm)
0 3,9,15 * * * cd /root/bdjob_scrap_automation && MAX_PAGES=10 /root/venv/bin/python bdgovtjob.py >> /root/bdgovtjob_scraper.log 2>&1
```

---

**Good luck! 🚀**

