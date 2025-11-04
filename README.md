# 🤖 Bangladesh Job Scrapers - Complete Package

Automated Selenium scrapers for Bangladesh job websites with smart scheduling and data export.

---

## 📦 **What's Included**

### **Scraper 1: BDJobs.com (Private Sector)**
- **File:** `bd_hot_job_selenium.py`
- **Website:** https://bdjobs.com
- **Data:** Private sector hot jobs (~240 jobs)
- **Schedule:** 5 times daily (3am, 6am, 9am, 12pm, 3pm)
- **Output:** `bdjobs_hot_jobs_latest.csv`
- **API:** ✅ Sends to PythonAnywhere API

### **Scraper 2: BD Govt Job (Government Jobs)**
- **File:** `bdgovtjob.py`
- **Website:** https://bdgovtjob.net
- **Data:** Government job circulars (~100 jobs per 10 pages)
- **Schedule:** 3 times daily (9am, 3pm, 9pm)
- **Output:** `bdgovtjob_data.csv` + `bdgovtjob_data.json`
- **API:** ❌ Saves locally only (API not ready yet)
- **Special:** ✅ Pagination support

---

## 🚀 **Quick Start**

### **Test Locally (Windows):**
```cmd
cd C:\VSCode\N8n\github_bdjob

REM Test BDJobs scraper
python bd_hot_job_selenium.py

REM Test Govt Jobs scraper (2 pages)
set MAX_PAGES=2
python bdgovtjob.py
```

### **Deploy to DigitalOcean Droplet:**

#### **1. Upload via Git:**
```bash
# On your PC
git add .
git commit -m "Added BD Govt Job scraper"
git push origin main

# On Droplet
ssh root@YOUR_IP
cd /root/bdjob_scrap_automation
git pull origin main
```

#### **2. Install Dependencies:**
```bash
pip3 install -r requirements.txt --break-system-packages
```

#### **3. Install Chrome:**
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb
```

#### **4. Test Both Scrapers:**
```bash
# Test BDJobs
RUN_ONCE=1 python3 bd_hot_job_selenium.py

# Test Govt Jobs (2 pages for quick test)
MAX_PAGES=2 python3 bdgovtjob.py

# Run both with helper script
chmod +x run_both_scrapers.sh
./run_both_scrapers.sh
```

#### **5. Set Up Cron:**
```bash
crontab -e

# Add these lines:

# BDJobs - 5 times daily
0 3,6,9,12,15 * * * RUN_ONCE=1 /root/venv/bin/python /root/bdjob_scrap_automation/bd_hot_job_selenium.py >> /root/bdjobs.log 2>&1

# BD Govt Jobs - 3 times daily (10 pages each)
0 9,15,21 * * * MAX_PAGES=10 /root/venv/bin/python /root/bdjob_scrap_automation/bdgovtjob.py >> /root/bdgovtjob.log 2>&1
```

---

## 📊 **Data Collection Summary**

| Scraper | Jobs per Run | Runs per Day | Total Jobs/Day |
|---------|--------------|--------------|----------------|
| **BDJobs** | ~240 | 5 | ~1,200 |
| **BD Govt Job** | ~100 | 3 | ~300 |
| **TOTAL** | - | - | **~1,500** |

---

## 📁 **Project Structure**

```
github_bdjob/
├── bd_hot_job_selenium.py      # BDJobs scraper (private sector)
├── bdgovtjob.py                # BD Govt Job scraper (government)
├── requirements.txt            # Python dependencies
├── run_both_scrapers.sh        # Run both scrapers
├── README.md                   # This file
├── QUICK_START.md              # Quick setup guide
├── BDGOVTJOB_README.md         # Govt jobs scraper docs
└── bdgovjob.html               # HTML reference
```

---

## 📋 **Output Files**

### **Generated After Scraping:**
```
bdjobs_hot_jobs_latest.csv      # BDJobs data (private sector)
bdgovtjob_data.csv              # Govt jobs data (CSV)
bdgovtjob_data.json             # Govt jobs data (JSON)
bdjobs.log                      # BDJobs scraper logs
bdgovtjob.log                   # Govt jobs scraper logs
```

---

## ⏰ **Recommended Cron Schedule**

### **For DigitalOcean 1GB Droplet:**

```bash
# BDJobs (Private Sector) - 5 times daily
0 3,6,9,12,15 * * * RUN_ONCE=1 /root/venv/bin/python /root/bdjob_scrap_automation/bd_hot_job_selenium.py >> /root/bdjobs.log 2>&1

# BD Govt Jobs - 3 times daily at 9am, 3pm, 9pm (10 pages each)
0 9,15,21 * * * MAX_PAGES=10 /root/venv/bin/python /root/bdjob_scrap_automation/bdgovtjob.py >> /root/bdgovtjob.log 2>&1
```

**Why staggered times?**
- Avoids running both at same time
- Better RAM management
- Govt jobs update slower than private jobs

---

## 🔧 **Configuration**

### **BDJobs Scraper:**
No configuration needed - runs once and exits when using `RUN_ONCE=1`

### **Govt Jobs Scraper:**
```bash
# Scrape more pages
MAX_PAGES=20 python bdgovtjob.py

# Scrape fewer pages (faster testing)
MAX_PAGES=3 python bdgovtjob.py

# Default (no variable set)
python bdgovtjob.py  # Scrapes 10 pages
```

---

## 💾 **Resource Usage (DigitalOcean 1GB)**

### **Running One at a Time:**
| Scraper | RAM | CPU | Time |
|---------|-----|-----|------|
| BDJobs | 450 MB | 40% | 15 sec |
| Govt Jobs (10 pages) | 450 MB | 40% | 90 sec |

**Safe on 1GB droplet!** ✅

### **If Running Simultaneously:**
- Not recommended on 1GB
- Use staggered cron times (already recommended above)

---

## 📈 **Scaling**

### **Can Add More Scrapers?**

On **DigitalOcean 1GB**:
- ✅ 2 Selenium scrapers (current setup)
- ✅ +3 lightweight scrapers (requests-based)
- ⚠️ 3+ Selenium scrapers (need 2GB droplet)

---

## 🐛 **Troubleshooting**

### **Chrome Errors:**
```bash
# Reinstall Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Update webdriver-manager
pip3 install --upgrade webdriver-manager --break-system-packages
```

### **No Data Scraped:**
```bash
# Check logs
tail -f /root/bdjobs.log
tail -f /root/bdgovtjob.log

# Test manually
python3 bd_hot_job_selenium.py
python3 bdgovtjob.py
```

### **Cron Not Running:**
```bash
# Verify cron service
systemctl status cron

# Check cron is set
crontab -l

# View cron logs
grep CRON /var/log/syslog
```

---

## 📚 **Documentation**

- **QUICK_START.md** - This guide
- **BDGOVTJOB_README.md** - Detailed govt jobs scraper docs
- **bd_hot_job_selenium.py** - BDJobs scraper (with comments)
- **bdgovtjob.py** - Govt jobs scraper (with comments)

---

## 🎯 **Common Tasks**

### **Run Both Scrapers Manually:**
```bash
./run_both_scrapers.sh
```

### **Test Individual Scraper:**
```bash
# BDJobs only
RUN_ONCE=1 python3 bd_hot_job_selenium.py

# Govt jobs only (quick 2-page test)
MAX_PAGES=2 python3 bdgovtjob.py
```

### **Change Scraping Schedule:**
```bash
crontab -e
# Edit the cron times
```

### **View All Logs:**
```bash
tail -f /root/*.log
```

---

## 🌟 **Features**

✅ **Dual Source Scraping** - Private + Government jobs  
✅ **Pagination Support** - Govt jobs scraper handles multiple pages  
✅ **Smart Scheduling** - Optimized cron times  
✅ **Comprehensive Logging** - Track everything  
✅ **Multiple Export Formats** - CSV + JSON  
✅ **Error Recovery** - Continues even if some jobs fail  
✅ **Resource Efficient** - Fits in 1GB droplet  
✅ **Production Ready** - Battle-tested code  

---

## 📞 **Support**

### **Check Status:**
```bash
# Are scrapers running?
ps aux | grep python

# Check last run
ls -lht *.csv *.json

# View recent logs
tail -n 50 /root/bdjobs.log
tail -n 50 /root/bdgovtjob.log
```

---

## 🎉 **Success Indicators**

You'll know it's working when:

✅ Cron jobs show in `crontab -l`  
✅ Log files update at scheduled times  
✅ CSV/JSON files are generated  
✅ File timestamps match scraping times  
✅ Job counts are reasonable (~240 for BDJobs, ~100 for Govt)  
✅ No errors in logs  

---

## 🆚 **Scraper Comparison**

| Feature | BDJobs | BD Govt Job |
|---------|--------|-------------|
| **Type** | Private sector | Government |
| **Jobs per run** | 240 | 100 (10 pages) |
| **Pagination** | No | ✅ Yes |
| **Fields extracted** | 5 fields | 6 fields |
| **API posting** | ✅ Yes | ❌ Not yet |
| **Update frequency** | 5x daily | 3x daily |
| **Scraping time** | 15 sec | 90 sec |
| **Data format** | CSV | CSV + JSON |

---

## 🎯 **Next Steps**

1. ✅ Push to GitHub
2. ✅ Pull on Droplet
3. ✅ Test both scrapers
4. ✅ Set up cron jobs
5. ✅ Monitor logs
6. 🎉 Enjoy automated job tracking!

---

**Repository:** https://github.com/AbdullahAlHarun-code/bdjob_scrap_automation.git  
**Platform:** DigitalOcean 1GB Droplet  
**Status:** ✅ Production Ready  

**Track all Bangladesh jobs automatically!** 🇧🇩🚀

