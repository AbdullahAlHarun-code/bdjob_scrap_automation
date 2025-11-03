import time
import requests
import json
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import os

class BDJobsHotJobsScraper:
    def __init__(self):
        self.base_url = "https://bdjobs.com/"
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present on the page"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def scrape_hot_jobs(self):
        """Scrape jobs from the Hot Jobs section"""
        print("Starting to scrape Hot Jobs section...")
        try:
            # Load the page
            self.driver.get(self.base_url)
            print("Page loaded, waiting for content...")
            
            # Wait for the Hot Jobs section to load
            hot_jobs_section = self.wait_for_element(By.CLASS_NAME, "m-text-center")
            print("Found Hot Jobs section!")

            # Wait a bit for all dynamic content to load
            time.sleep(5)

            # Get all job cards
            job_cards = self.driver.find_elements(By.CLASS_NAME, "c-card")
            all_jobs = []

            print(f"Found {len(job_cards)} job cards")
            for card in job_cards:
                try:
                    # Get company logo
                    try:
                        logo = card.find_element(By.CSS_SELECTOR, ".companyLogo img")
                        logo_url = logo.get_attribute('src')
                    except:
                        logo_url = 'N/A'

                    # Get company name
                    try:
                        company_name_spans = card.find_elements(By.CSS_SELECTOR, "h3 .wr")
                        company_name = ' '.join([span.text for span in company_name_spans])
                    except:
                        company_name = 'N/A'

                    # Get job positions
                    job_links = card.find_elements(By.CSS_SELECTOR, ".companyDetails li a")
                    
                    for job_link in job_links:
                        position_spans = job_link.find_elements(By.CLASS_NAME, "wr")
                        position = ' '.join([span.text for span in position_spans])
                        job_url = job_link.get_attribute('href')
                        
                        job_data = {
                            'company_name': company_name,
                            'company_logo_url': logo_url,
                            'position': position,
                            'job_url': job_url,
                            'scraped_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        all_jobs.append(job_data)
                        print(f"Scraped: {job_data['company_name']} - {job_data['position']}")

                except Exception as e:
                    print(f"Error processing job card: {e}")
                    continue

            return all_jobs

        except Exception as e:
            print(f"Error during scraping: {e}")
            return []
        
        finally:
            self.driver.quit()

    def save_to_csv(self, jobs, filename='bdjobs_hot_jobs.csv'):
        """Save scraped data to CSV"""
        if jobs:
            df = pd.DataFrame(jobs)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\nData saved to {os.path.abspath(filename)}")
            print(f"Total hot jobs scraped: {len(jobs)}")
        else:
            print("No jobs to save")

def main():
    # Initialize scraper
    scraper = BDJobsHotJobsScraper()
    
    # Scrape hot jobs
    print("Starting the scraping process...")
    jobs = scraper.scrape_hot_jobs()
    
    # Save results to CSV
    scraper.save_to_csv(jobs)


def send_jobs_to_api(jobs, api_url="https://abdullah007ie.pythonanywhere.com/n8n/send-data/"):
    """POST jobs (list) to configured API endpoint."""
    if not jobs:
        print("No jobs to send")
        return

    api_url = api_url or os.environ.get('HOT_JOBS_API_URL', 'http://127.0.0.1:8000/n8n/send-data/')
    try:
        print(f"Posting {len(jobs)} jobs to {api_url}...")
        resp = requests.post(api_url, json=jobs, timeout=30)
        print(f"API response: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Error posting to API: {e}")


def job_runner():
    """Runner for scheduler: scrape and POST."""
    print(f"Runner triggered at {datetime.now()}\n")
    scraper = BDJobsHotJobsScraper()
    jobs = scraper.scrape_hot_jobs()
    # Optionally save locally
    scraper.save_to_csv(jobs, filename='bdjobs_hot_jobs_latest.csv')
    send_jobs_to_api(jobs)


def schedule_every_5_minutes():
    sched = BlockingScheduler()
    # run immediately once, then every 60 minutes
    sched.add_job(job_runner, 'interval', minutes=60, next_run_time=datetime.now())
    print("Scheduler started: running job every 60 minutes")
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped")


if __name__ == "__main__":
    # If you want to run once, set RUN_ONCE env var to '1'
    if os.environ.get('RUN_ONCE') == '1':
        main()
    else:
        schedule_every_5_minutes()
