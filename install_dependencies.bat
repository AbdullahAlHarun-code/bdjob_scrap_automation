@echo off
echo ============================================================
echo BD GOVT JOB SCRAPER - DEPENDENCY INSTALLER
echo ============================================================
echo.
echo Installing required Python packages...
echo.

python -m pip install --upgrade pip
python -m pip install selenium
python -m pip install pandas  
python -m pip install webdriver-manager
python -m pip install beautifulsoup4
python -m pip install lxml
python -m pip install requests
python -m pip install APScheduler
python -m pip install urllib3

echo.
echo ============================================================
echo Testing installation...
echo ============================================================
echo.

python test_scraper.py

echo.
echo ============================================================
echo Installation complete!
echo.
echo To run the scraper:
echo   python bdgovtjob.py
echo ============================================================
echo.
pause

