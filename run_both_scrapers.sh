#!/bin/bash
# Run both BDJobs and BD Govt Job scrapers
# This script runs both scrapers sequentially

echo "╔════════════════════════════════════════════════════════════╗"
echo "║          RUNNING ALL JOB SCRAPERS                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Use virtual environment if available
if [ -d "/root/venv" ]; then
    PYTHON="/root/venv/bin/python"
    echo "✓ Using virtual environment"
else
    PYTHON="python3"
    echo "✓ Using system Python"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "1/2: Scraping BDJobs.com (Private Sector Jobs)"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Run BDJobs scraper
RUN_ONCE=1 $PYTHON bd_hot_job_selenium.py

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "2/2: Scraping BDGovtJob.net (Government Jobs)"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Run BD Govt Job scraper (10 pages by default)
MAX_PAGES=10 $PYTHON bdgovtjob.py

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║               ALL SCRAPERS COMPLETED! ✅                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Output Files:"
echo "   - bdjobs_hot_jobs_latest.csv     (Private sector jobs)"
echo "   - bdgovtjob_data.csv             (Government jobs)"
echo "   - bdgovtjob_data.json            (Government jobs)"
echo ""
echo "🎉 Done!"

