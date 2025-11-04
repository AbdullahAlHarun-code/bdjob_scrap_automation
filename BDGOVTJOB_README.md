# 🏛️ BD Govt Job Scraper

Selenium-based scraper for Bangladesh Government Job Circulars from https://bdgovtjob.net

---

## ✨ Features

- ✅ **Pagination Support** - Scrapes multiple pages automatically
- ✅ **Complete Data Extraction** - Title, organization, vacancies, deadline, etc.
- ✅ **Dual Export** - Saves to both CSV and JSON
- ✅ **Smart Organization Detection** - Extracts org name from title
- ✅ **Error Handling** - Continues even if some jobs fail
- ✅ **Progress Tracking** - Shows real-time scraping progress
- ✅ **Configurable** - Set max pages via environment variable

---

## 📊 Data Extracted

For each government job circular, extracts **6 essential fields**:

| Field | Description | Example |
|-------|-------------|---------|
| `job_title` | Full job title | "Planning Division Job Circular 2025 plandiv.teletalk.com.bd" |
| `job_url` | Link to full circular | "https://bdgovtjob.net/planning-division-job-circular/" |
| `vacancies` | Number of positions | "65" |
| `deadline` | Application deadline | "25 November 2025 at 5:00 PM" |
| `posted_date` | Posted date | "3 November, 2025" |
| `scraped_at` | When scraped | "2025-11-03 10:30:00" |

---

## 🚀 Usage

### **Basic Run (Scrapes 10 pages):**
```bash
python bdgovtjob.py
```

### **Custom Number of Pages:**
```bash
# Scrape 5 pages
MAX_PAGES=5 python bdgovtjob.py

# Scrape 20 pages
MAX_PAGES=20 python bdgovtjob.py

# Scrape all pages (set high number)
MAX_PAGES=100 python bdgovtjob.py
```

### **On DigitalOcean Droplet:**
```bash
# With virtual environment
/root/venv/bin/python bdgovtjob.py

# Custom pages
MAX_PAGES=15 /root/venv/bin/python bdgovtjob.py
```

---

## 📁 Output Files

### **CSV Format:** `bdgovtjob_data.csv`
```csv
job_title,job_url,vacancies,deadline,posted_date,scraped_at
Planning Division Job Circular 2025,https://bdgovtjob.net/planning-division-job-circular/,65,25 November 2025 at 5:00 PM,3 November 2025,2025-11-03 10:30:00
```

### **JSON Format:** `bdgovtjob_data.json`
```json
[
  {
    "job_title": "Planning Division Job Circular 2025 plandiv.teletalk.com.bd",
    "job_url": "https://bdgovtjob.net/planning-division-job-circular/",
    "vacancies": "65",
    "deadline": "25 November 2025 at 5:00 PM",
    "posted_date": "3 November, 2025",
    "scraped_at": "2025-11-03 10:30:00"
  }
]
```

---

## ⏱ **Performance**

### **Estimated Times:**

| Pages | Jobs (approx) | Time | RAM Usage |
|-------|---------------|------|-----------|
| 1 page | ~10 jobs | 10 sec | 450 MB |
| 5 pages | ~50 jobs | 45 sec | 450 MB |
| 10 pages | ~100 jobs | 90 sec | 450 MB |
| 20 pages | ~200 jobs | 3 min | 450 MB |

**Note:** Each page takes ~8-10 seconds including navigation.

---

## 🔧 Configuration

### **Environment Variables:**

```bash
# Maximum pages to scrape (default: 10)
export MAX_PAGES=20

# Run the scraper
python bdgovtjob.py
```

### **Modify Timeouts:**

Edit `bdgovtjob.py` line 51:
```python
time.sleep(3)  # Page load wait time
```

Edit line 125:
```python
time.sleep(3)  # Next page navigation wait
```

---

## 📅 **Schedule with Cron**

### **Run Daily at 9am:**
```bash
crontab -e

# Add this line:
0 9 * * * cd /root/bdjob_scrap_automation && /root/venv/bin/python bdgovtjob.py >> bdgovtjob.log 2>&1
```

### **Run 3 Times Daily (9am, 3pm, 9pm):**
```bash
0 9,15,21 * * * cd /root/bdjob_scrap_automation && /root/venv/bin/python bdgovtjob.py >> bdgovtjob.log 2>&1
```

### **Run Every 6 Hours:**
```bash
0 */6 * * * cd /root/bdjob_scrap_automation && /root/venv/bin/python bdgovtjob.py >> bdgovtjob.log 2>&1
```

---

## 🐛 Troubleshooting

### **No jobs found:**
- Check if website is accessible: https://bdgovtjob.net/category/government-jobs-circular/
- Verify Chrome/ChromeDriver installed
- Check internet connection
- Try increasing wait time (line 51)

### **Pagination not working:**
- Website might have changed pagination structure
- Check browser console for JavaScript errors
- Try manual navigation to verify pagination exists

### **ChromeDriver errors:**
```bash
# Update ChromeDriver
pip install --upgrade webdriver-manager

# Or install Chrome manually:
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb
```

### **Memory issues:**
- Reduce MAX_PAGES
- Run during off-peak hours
- Increase droplet RAM if needed

---

## 📊 Expected Output

```
🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷
  BD GOVT JOB SCRAPER
  https://bdgovtjob.net
🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷

============================================================
🚀 BD GOVT JOB SCRAPER - STARTING
============================================================
Target: https://bdgovtjob.net/category/government-jobs-circular/
Max pages: 10
============================================================

📡 Loading https://bdgovtjob.net/category/government-jobs-circular/...
✅ Page loaded successfully!

============================================================
📄 Scraping Page 1
============================================================
Found 10 job articles on page 1
  ✓ [1/10] Planning Division Job Circular 2025...
  ✓ [2/10] Bangladesh Bank Job Circular 2025...
  ✓ [3/10] Ministry of Education Job Circular...
  ...
✅ Page 1 complete: 10 jobs extracted

➡ Attempting to navigate to page 2...
  ➡ Clicked next page button

============================================================
📄 Scraping Page 2
============================================================
Found 10 job articles on page 2
  ✓ [1/10] Health Ministry Job Circular...
  ...

[... continues for all pages ...]

============================================================
✅ SCRAPING COMPLETE!
Total pages scraped: 10
Total jobs collected: 100
============================================================

✅ CSV saved: /root/bdjob_scrap_automation/bdgovtjob_data.csv
   Rows: 100
✅ JSON saved: /root/bdjob_scrap_automation/bdgovtjob_data.json
   Records: 100

============================================================
🎉 SUCCESS! Data saved to:
   📄 bdgovtjob_data.csv
   📄 bdgovtjob_data.json
============================================================

📊 SUMMARY:
   Total jobs: 100
   Jobs with vacancy info: 95
   Total vacancies: 1850
   Jobs with deadline: 98

✅ Scraper finished!
```

---

## 🔄 Integration with Existing Workflow

### **Run Both Scrapers:**

```bash
# BDJobs (every 20 minutes)
*/20 * * * * RUN_ONCE=1 /root/venv/bin/python /root/bdjob_scrap_automation/bd_hot_job_selenium.py >> /root/bdjobs.log 2>&1

# BD Govt Jobs (3 times daily)
0 9,15,21 * * * MAX_PAGES=10 /root/venv/bin/python /root/bdjob_scrap_automation/bdgovtjob.py >> /root/bdgovtjob.log 2>&1
```

---

## 💡 **Tips**

### **Start Small:**
```bash
# Test with 2 pages first
MAX_PAGES=2 python bdgovtjob.py
```

### **Monitor Progress:**
```bash
# Watch logs in real-time
tail -f bdgovtjob.log
```

### **Check Data:**
```bash
# Count records
wc -l bdgovtjob_data.csv

# View first 10 jobs
head -n 11 bdgovtjob_data.csv
```

---

## 📈 Pagination Strategy

The scraper:
1. Loads first page
2. Scrapes all jobs on current page
3. Looks for "Next" button
4. Clicks it if found
5. Waits for page load
6. Repeats steps 2-5
7. Stops when:
   - No next button found
   - Max pages reached
   - No jobs found on page

---

## 🎯 **Recommended Settings:**

### **For Daily Updates:**
```bash
MAX_PAGES=5  # ~50 recent jobs
```

### **For Initial Scrape:**
```bash
MAX_PAGES=50  # Get historical data
```

### **For Quick Test:**
```bash
MAX_PAGES=2  # Just test it works
```

---

## 📞 Support

### **Check Logs:**
```bash
cat bdgovtjob.log
```

### **Test Manually:**
```bash
python bdgovtjob.py
```

### **Verify Chrome:**
```bash
google-chrome --version
chromedriver --version
```

---

## 🆚 Comparison with BDJobs Scraper

| Feature | BDJobs | BD Govt Job |
|---------|--------|-------------|
| **Website** | bdjobs.com | bdgovtjob.net |
| **Data Type** | Private sector | Government jobs |
| **Update Frequency** | Every 20 min | 3x daily |
| **Pagination** | No | ✅ Yes |
| **Jobs per Page** | 140+ | ~10 |
| **Scraping Time** | 15 sec | 90 sec (10 pages) |

---

## 🎉 **Ready to Use!**

```bash
# Quick test
python bdgovtjob.py

# Check output
ls -lh bdgovtjob_data.*
```

**That's it!** 🚀

---

**File:** `bdgovtjob.py`  
**Version:** 1.0.0  
**Author:** Automated Scraper  
**Last Updated:** November 2025

