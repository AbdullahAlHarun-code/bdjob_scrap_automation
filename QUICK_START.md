# ⚡ Quick Start - Two Scrapers Setup

## 🎯 You Now Have 2 Scrapers!

### **1. BDJobs.com Scraper** (`bd_hot_job_selenium.py`)
- **Website:** https://bdjobs.com
- **Type:** Private sector hot jobs
- **Schedule:** Every 20 minutes OR 5x daily
- **Output:** `bdjobs_hot_jobs_latest.csv`

### **2. BD Govt Job Scraper** (`bdgovtjob.py`)
- **Website:** https://bdgovtjob.net
- **Type:** Government job circulars
- **Schedule:** Daily or 3x daily
- **Output:** `bdgovtjob_data.csv` + `bdgovtjob_data.json`
- **Pagination:** ✅ Scrapes multiple pages

---

## 🚀 **Quick Test (Local):**

```bash
cd C:\VSCode\N8n\github_bdjob

# Test BDJobs scraper
python bd_hot_job_selenium.py

# Test Govt Jobs scraper (2 pages)
set MAX_PAGES=2
python bdgovtjob.py

# Run both
run_both_scrapers.sh  # Linux/Mac
```

---

## 🌐 **Deploy to DigitalOcean Droplet:**

### **1. Upload Files:**

```bash
# On your PC (Windows)
cd C:\VSCode\N8n\github_bdjob

# Commit to GitHub
git add .
git commit -m "Added BD Govt Job scraper with pagination"
git push origin main

# On Droplet
ssh root@YOUR_DROPLET_IP
cd /root/bdjob_scrap_automation
git pull origin main
```

### **2. Test Both Scrapers:**

```bash
# Test BDJobs scraper
RUN_ONCE=1 /root/venv/bin/python bd_hot_job_selenium.py

# Test Govt Jobs scraper (2 pages for quick test)
MAX_PAGES=2 /root/venv/bin/python bdgovtjob.py

# Run both with helper script
chmod +x run_both_scrapers.sh
./run_both_scrapers.sh
```

### **3. Set Up Cron Jobs:**

```bash
crontab -e

# Add these lines:

# BDJobs - 5 times daily (3am, 6am, 9am, 12pm, 3pm)
0 3,6,9,12,15 * * * RUN_ONCE=1 /root/venv/bin/python /root/bdjob_scrap_automation/bd_hot_job_selenium.py >> /root/bdjobs.log 2>&1

# BD Govt Jobs - 3 times daily (9am, 3pm, 9pm) with 10 pages
0 9,15,21 * * * MAX_PAGES=10 /root/venv/bin/python /root/bdjob_scrap_automation/bdgovtjob.py >> /root/bdgovtjob.log 2>&1

# Save: Ctrl+X, Y, Enter
```

---

## 📊 **What Gets Scraped:**

### **BDJobs.com:**
- ~240 private sector hot jobs
- Company name, logo, position, URL
- Updates 5x daily

### **BDGovtJob.net:**
- ~100 government circulars (10 pages)
- Job title, organization, vacancies, deadline
- Updates 3x daily

**Total: ~340 jobs tracked daily!** 🎉

---

## 📁 **Output Files:**

```
bdjob_scrap_automation/
├── bdjobs_hot_jobs_latest.csv    ← Private sector jobs
├── bdgovtjob_data.csv             ← Govt jobs (CSV)
├── bdgovtjob_data.json            ← Govt jobs (JSON)
├── bdjobs.log                     ← BDJobs logs
└── bdgovtjob.log                  ← Govt jobs logs
```

---

## 🔍 **Monitor Scrapers:**

### **Check Logs:**
```bash
# BDJobs logs
tail -f /root/bdjobs.log

# Govt Jobs logs
tail -f /root/bdgovtjob.log

# Both at once
tail -f /root/*.log
```

### **Check Output Files:**
```bash
# Count jobs
wc -l bdgovtjob_data.csv
wc -l bdjobs_hot_jobs_latest.csv

# View recent data
tail -n 5 bdgovtjob_data.csv
```

### **Verify Cron:**
```bash
# List all cron jobs
crontab -l

# Check cron service is running
systemctl status cron
```

---

## 🎯 **Recommended Schedule:**

```bash
# BDJobs (Private Sector) - 5 times daily
0 3,6,9,12,15 * * * → bd_hot_job_selenium.py

# BD Govt Jobs - 3 times daily (scrapes 10 pages each)
0 9,15,21 * * * → bdgovtjob.py (MAX_PAGES=10)
```

**Why this schedule?**
- Private jobs change frequently → Check 5x daily
- Govt jobs change slower → Check 3x daily
- Staggered times → Better resource usage

---

## 💾 **Storage Estimates:**

### **Per Day:**
- BDJobs CSV: ~60 KB × 5 = 300 KB/day
- Govt Jobs CSV: ~50 KB × 3 = 150 KB/day
- Govt Jobs JSON: ~80 KB × 3 = 240 KB/day
- **Total: ~700 KB/day**

### **Per Month:**
- ~21 MB/month
- Easily fits in 25GB SSD

---

## 🎉 **Complete Setup Checklist:**

- [ ] Both scripts uploaded to droplet
- [ ] Chrome/ChromeDriver installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] BDJobs scraper tested
- [ ] Govt Jobs scraper tested
- [ ] Cron jobs configured
- [ ] Logs monitored for first run
- [ ] Output files verified

---

## 🔥 **One-Command Setup (Droplet):**

```bash
# Run this on your droplet to set everything up

cd /root/bdjob_scrap_automation

# Make helper script executable
chmod +x run_both_scrapers.sh

# Test both scrapers
./run_both_scrapers.sh

# If successful, set up cron (use the commands above)
```

---

## 📞 **Need Help?**

**Check documentation:**
- `BDGOVTJOB_README.md` - Govt jobs scraper guide
- `bd_hot_job_selenium.py` - BDJobs scraper

**Common issues:**
- Chrome not installed → Install Chrome
- Module not found → `pip install -r requirements.txt --break-system-packages`
- No data scraped → Check logs for errors
- Pagination not working → Reduce MAX_PAGES, check website

---

**You're all set! Run both scrapers and track all Bangladesh jobs!** 🎉🇧🇩

