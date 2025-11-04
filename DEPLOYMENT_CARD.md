# 🚀 Quick Deployment Card - DigitalOcean Droplet

## 📋 **Copy-Paste Commands for Droplet Setup**

---

## 1️⃣ **INITIAL SETUP (One-Time)**

### **On Droplet:**
```bash
# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Create virtual environment
apt install python3-venv python3-full -y
python3 -m venv /root/venv

# Clone repository
cd /root
git clone https://github.com/AbdullahAlHarun-code/bdjob_scrap_automation.git
cd bdjob_scrap_automation

# Activate venv and install dependencies
source /root/venv/bin/activate
pip install -r requirements.txt
```

---

## 2️⃣ **TEST SCRAPERS**

```bash
# Test BDJobs scraper
RUN_ONCE=1 /root/venv/bin/python bd_hot_job_selenium.py

# Test Govt Jobs scraper (2 pages for quick test)
MAX_PAGES=2 /root/venv/bin/python bdgovtjob.py

# Test both
chmod +x run_both_scrapers.sh
./run_both_scrapers.sh
```

---

## 3️⃣ **SET UP CRON SCHEDULE**

```bash
crontab -e
# Choose: 1 (nano)
```

**Add these lines:**
```
# BDJobs - 5 times daily (3am, 6am, 9am, 12pm, 3pm)
0 3,6,9,12,15 * * * RUN_ONCE=1 /root/venv/bin/python /root/bdjob_scrap_automation/bd_hot_job_selenium.py >> /root/bdjobs.log 2>&1

# BD Govt Jobs - 3 times daily (9am, 3pm, 9pm) with 10 pages
0 9,15,21 * * * MAX_PAGES=10 /root/venv/bin/python /root/bdjob_scrap_automation/bdgovtjob.py >> /root/bdgovtjob.log 2>&1
```

**Save:** Ctrl+X, Y, Enter

---

## 4️⃣ **VERIFY SETUP**

```bash
# Check cron is set
crontab -l

# Check output files exist (after first run)
ls -lh /root/bdjob_scrap_automation/*.csv
ls -lh /root/bdjob_scrap_automation/*.json

# Monitor logs
tail -f /root/bdjobs.log
tail -f /root/bdgovtjob.log
```

---

## 🔄 **UPDATE CODE (When You Change)**

```bash
# On Droplet
cd /root/bdjob_scrap_automation
git pull origin main

# Cron will automatically use new code on next run!
```

---

## 📊 **MONITORING COMMANDS**

```bash
# View logs
tail -n 50 /root/bdjobs.log
tail -n 50 /root/bdgovtjob.log

# Check if scrapers are running
ps aux | grep python

# Check cron schedule
crontab -l

# Check last file updates
ls -lht /root/bdjob_scrap_automation/*.csv

# View recent data
tail -n 10 /root/bdjob_scrap_automation/bdgovtjob_data.csv
```

---

## 🎯 **SCRAPING SCHEDULE:**

| Time | Scraper | Jobs |
|------|---------|------|
| 03:00 | BDJobs | ~240 |
| 06:00 | BDJobs | ~240 |
| 09:00 | BDJobs + Govt Jobs | ~340 |
| 12:00 | BDJobs | ~240 |
| 15:00 | BDJobs + Govt Jobs | ~340 |
| 21:00 | Govt Jobs | ~100 |

**Total Daily:** ~1,500 jobs tracked!

---

## 🔧 **QUICK FIXES:**

### **Scraper not running:**
```bash
# Restart cron
systemctl restart cron

# Check cron status
systemctl status cron
```

### **No data in files:**
```bash
# Run manually to see errors
cd /root/bdjob_scrap_automation
/root/venv/bin/python bd_hot_job_selenium.py
MAX_PAGES=2 /root/venv/bin/python bdgovtjob.py
```

### **Chrome not found:**
```bash
# Reinstall Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb
```

---

## 💡 **TIPS:**

- Start with MAX_PAGES=5 for govt jobs, increase later
- Monitor logs first 24 hours
- Check CSV file sizes to verify data
- Use `git pull` to update easily

---

## ✅ **SUCCESS CHECKLIST:**

- [ ] Droplet created (1GB, $6/month)
- [ ] Chrome installed
- [ ] Virtual environment created
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Both scrapers tested
- [ ] Cron jobs configured
- [ ] Logs monitored
- [ ] Output files verified
- [ ] Schedule confirmed

---

## 🎉 **DONE!**

**Save this card for quick reference!**

**Status:** ✅ Production Ready  
**Platform:** DigitalOcean 1GB Droplet  
**Cost:** $6/month  
**Jobs Tracked:** ~1,500/day  

