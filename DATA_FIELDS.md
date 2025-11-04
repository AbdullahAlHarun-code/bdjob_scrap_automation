# 📊 Data Fields Extracted

## Simple and Clean - Only Essential Information

---

## 🏛️ **BD Govt Job Data (6 Fields)**

From: https://bdgovtjob.net/category/government-jobs-circular/

### **Fields:**

| # | Field | Source HTML | Example |
|---|-------|-------------|---------|
| 1 | `job_title` | `h2.entry-title a` text | "Planning Division Job Circular 2025 plandiv.teletalk.com.bd" |
| 2 | `job_url` | `h2.entry-title a` href | "https://bdgovtjob.net/planning-division-job-circular/" |
| 3 | `vacancies` | `.job-vacancy .job-value` | "65" |
| 4 | `deadline` | `.job-deadline .job-value` | "25 November 2025 at 5:00 PM" |
| 5 | `posted_date` | `time.entry-date.published` | "3 November, 2025" |
| 6 | `scraped_at` | Current datetime | "2025-11-03 10:30:00" |

---

## 🏢 **BDJobs Data (5 Fields)**

From: https://bdjobs.com/

### **Fields:**

| # | Field | Source HTML | Example |
|---|-------|-------------|---------|
| 1 | `company_name` | `h3 .wr` spans | "BRAC Bank PLC" |
| 2 | `company_logo_url` | `.companyLogo img` src | "https://hotjobs.bdjobs.com/logos/bracbank300-min.png" |
| 3 | `position` | `.companyDetails a .wr` spans | "ESG Analyst, ESG and Sustainable Finance" |
| 4 | `job_url` | `.companyDetails a` href | "https://hotjobs.bdjobs.com/jobs/bracbank/bracbank859.htm" |
| 5 | `scraped_date` | Current datetime | "2025-11-03 12:00:00" |

---

## 📋 **CSV Output Examples:**

### **bdgovtjob_data.csv:**
```csv
job_title,job_url,vacancies,deadline,posted_date,scraped_at
Planning Division Job Circular 2025,https://bdgovtjob.net/planning-division-job-circular/,65,25 November 2025 at 5:00 PM,3 November 2025,2025-11-03 10:30:00
Bangladesh Bank Job Circular 2025,https://bdgovtjob.net/bangladesh-bank-job/,125,30 November 2025,2 November 2025,2025-11-03 10:30:15
```

### **bdjobs_hot_jobs_latest.csv:**
```csv
company_name,company_logo_url,position,job_url,scraped_date
BRAC Bank PLC,https://hotjobs.bdjobs.com/logos/bracbank300-min.png,ESG Analyst...,https://hotjobs.bdjobs.com/jobs/bracbank/bracbank859.htm,2025-11-03 12:00:00
International Rescue Committee,https://hotjobs.bdjobs.com/logos/irclogo300a-min.png,Communication Expert,https://hotjobs.bdjobs.com/jobs/irc/irc694.htm,2025-11-03 12:00:05
```

---

## 🎯 **Field Mapping for API (Future)**

When you're ready to send govt jobs to API, you'll need to map:

```python
# BD Govt Job → API format
{
    "job_title": job_title,           # Direct mapping
    "job_url": job_url,                # Direct mapping
    "vacancies": vacancies,            # NEW field for API
    "deadline": deadline,              # NEW field for API
    "posted_date": posted_date,        # Can map to scraped_date
    "scraped_at": scraped_at,          # Timestamp
}
```

**API needs to add these fields:**
- `vacancies` (IntegerField or CharField)
- `deadline` (DateTimeField or CharField)

---

## 📊 **Data Statistics:**

### **BD Govt Jobs (per 10 pages):**
- Jobs: ~100
- With vacancies: ~95 (95%)
- With deadlines: ~98 (98%)
- Total positions: ~1,500-2,000 vacancies

### **BDJobs (per scrape):**
- Jobs: ~240
- Always has company, position, URL

---

## 🔍 **Data Quality:**

### **BD Govt Job:**
- **job_title:** ✅ Always available
- **job_url:** ✅ Always available
- **vacancies:** ⚠️ Sometimes N/A (~5%)
- **deadline:** ⚠️ Sometimes N/A (~2%)
- **posted_date:** ✅ Always available
- **scraped_at:** ✅ Always available

### **BDJobs:**
- **company_name:** ✅ Always available
- **company_logo_url:** ⚠️ Sometimes N/A
- **position:** ✅ Always available
- **job_url:** ✅ Always available
- **scraped_date:** ✅ Always available

---

## 💾 **File Sizes:**

### **BD Govt Jobs (100 records):**
- CSV: ~15 KB
- JSON: ~25 KB

### **BDJobs (240 records):**
- CSV: ~30 KB

**Total per day:** ~100 KB of data

---

## 🎯 **Field Usage:**

### **For Job Boards:**
- Display: job_title, vacancies, deadline
- Link: job_url
- Metadata: posted_date, scraped_at

### **For Analytics:**
- Track: Total vacancies over time
- Analyze: Deadline patterns
- Monitor: Posting frequency

### **For Alerts:**
- Filter: By deadline proximity
- Match: By vacancy count
- Sort: By posted_date

---

## ✅ **Summary:**

**BD Govt Job Scraper extracts 6 clean fields:**
1. job_title ✅
2. job_url ✅
3. vacancies ✅
4. deadline ✅
5. posted_date ✅
6. scraped_at ✅

**Simple, clean, essential data only!** 🎯

