import time
import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime

class BDGovtJobScraper:
    def __init__(self):
        self.base_url = "https://bdgovtjob.net/category/government-jobs-circular/"
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        self.all_jobs = []
    
    def get_page_url(self, page_num):
        """Generate URL for a specific page number"""
        if page_num == 1:
            return self.base_url
        else:
            return f"{self.base_url}page/{page_num}/"

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present on the page"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            print(f"Timeout waiting for element: {value}")
            return None

    def extract_link_text(self, el):
        """
        Extract text from a link element using multiple fallback methods
        1) Normal Selenium .text (visible text)
        2) DOM text properties (innerText, textContent)
        3) Useful attributes (aria-label, title)
        """
        # 1) Normal Selenium text (visible text)
        t = el.text.strip()
        if t:
            return t
        
        # 2) DOM text properties
        for attr in ("innerText", "textContent"):
            t = (el.get_attribute(attr) or "").strip()
            if t:
                return " ".join(t.split())  # normalize whitespace
        
        # 3) Useful attributes some themes set
        for attr in ("aria-label", "title"):
            t = (el.get_attribute(attr) or "").strip()
            if t:
                return t
        
        # 4) As a last resort, peek at innerHTML (for debugging)
        # print(f"DEBUG innerHTML: {el.get_attribute('innerHTML')}")
        return ""
    
    def extract_text_safe(self, element, selector, by=By.CSS_SELECTOR):
        """Safely extract text from element using multiple methods"""
        try:
            elem = element.find_element(by, selector)
            return self.extract_link_text(elem) or 'N/A'
        except NoSuchElementException:
            return 'N/A'
        except Exception as e:
            return 'N/A'

    def extract_attribute_safe(self, element, selector, attribute, by=By.CSS_SELECTOR):
        """Safely extract attribute from element"""
        try:
            elem = element.find_element(by, selector)
            return elem.get_attribute(attribute)
        except NoSuchElementException:
            return 'N/A'
        except Exception as e:
            return 'N/A'

    def scrape_page(self, page_num=1):
        """Scrape a single page of job listings"""
        print(f"\n{'='*60}")
        print(f"📄 Scraping Page {page_num}")
        print(f"{'='*60}")
        
        try:
            # Wait longer for dynamic content to load
            time.sleep(5)
            
            # Wait for articles to be present
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.post"))
                )
            except TimeoutException:
                print(f"⚠ Timeout waiting for articles on page {page_num}")
            
            # Find all job article elements
            articles = self.driver.find_elements(By.CSS_SELECTOR, "article.post")
            
            if not articles:
                print(f"⚠ No articles found on page {page_num}")
                return 0
            
            print(f"Found {len(articles)} job articles on page {page_num}")
            
            for idx, article in enumerate(articles, 1):
                try:
                    # Extract job title and URL - using improved text extraction
                    job_title = ''
                    job_url = ''
                    
                    # Try multiple selectors
                    try:
                        title_elem = article.find_element(By.CSS_SELECTOR, "h2.entry-title a, .entry-title a, header.entry-header a")
                        job_url = title_elem.get_attribute('href') or ""
                        job_title = self.extract_link_text(title_elem) or "N/A"
                    except Exception as e:
                        job_url, job_title = "", "N/A"
                    
                    # Extract posted date - using improved extraction
                    posted_date = self.extract_text_safe(article, "time.published, time.entry-date, .posted-on time")
                    
                    # Extract vacancies - using improved extraction
                    vacancies = self.extract_text_safe(article, ".job-vacancy .job-value, .job-info-box.job-vacancy .job-value")
                    
                    # Extract deadline - using improved extraction
                    deadline = self.extract_text_safe(article, ".job-deadline .job-value, .job-info-box.job-deadline .job-value")
                    
                    # Skip if no title or URL (critical fields)
                    if not job_title or not job_url:
                        print(f"  ⚠ [{idx}/{len(articles)}] Skipped - Missing title or URL")
                        continue
                    
                    # Create job data dictionary - ONLY essential fields
                    job_data = {
                        'job_title': job_title,
                        'job_url': job_url,
                        'vacancies': vacancies,
                        'deadline': deadline,
                        'posted_date': posted_date,
                        'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    self.all_jobs.append(job_data)
                    print(f"  ✓ [{idx}/{len(articles)}] {job_title[:60]}... | V:{vacancies} | D:{deadline[:15]}...")
                    
                except Exception as e:
                    print(f"  ✗ Error processing article {idx}: {e}")
                    continue
            
            print(f"✅ Page {page_num} complete: {len(articles)} jobs extracted")
            return len(articles)
            
        except Exception as e:
            print(f"❌ Error scraping page {page_num}: {e}")
            return 0

    def find_and_click_next_page(self):
        """Find and click the next page button"""
        try:
            # Common pagination selectors
            next_selectors = [
                "a.next.page-numbers",
                ".nav-links a.next",
                ".pagination a.next",
                "a[rel='next']",
                ".wp-pagenavi a.nextpostslink"
            ]
            
            for selector in next_selectors:
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if next_button:
                        # Scroll to button
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                        time.sleep(1)
                        
                        # Click it
                        next_button.click()
                        print("  ➡ Clicked next page button")
                        time.sleep(3)  # Wait for page to load
                        return True
                except NoSuchElementException:
                    continue
            
            print("  ℹ No next page button found")
            return False
            
        except Exception as e:
            print(f"  ⚠ Error finding next page: {e}")
            return False

    def scrape_all_pages(self, max_pages=10):
        """Scrape multiple pages by directly navigating to each page URL"""
        print("\n" + "="*60)
        print("🚀 BD GOVT JOB SCRAPER - STARTING")
        print("="*60)
        print(f"Target: {self.base_url}")
        print(f"Max pages: {max_pages}")
        print(f"Method: Direct URL navigation")
        print("="*60)
        
        try:
            # Loop through each page number and navigate directly
            for page_num in range(1, max_pages + 1):
                # Generate URL for this page
                page_url = self.get_page_url(page_num)
                
                # Load the page
                print(f"\n📡 Loading page {page_num}: {page_url}...")
                self.driver.get(page_url)
                print(f"✅ Page {page_num} loaded!")
                
                # Save debug HTML for first page only
                if page_num == 1:
                    try:
                        time.sleep(3)
                        page_source = self.driver.page_source
                        with open('debug_bdgovtjob_page.html', 'w', encoding='utf-8') as f:
                            f.write(page_source)
                        print("📝 DEBUG: Saved page 1 HTML to 'debug_bdgovtjob_page.html'")
                    except Exception as e:
                        print(f"⚠ Could not save debug HTML: {e}")
                
                # Scrape current page
                jobs_found = self.scrape_page(page_num)
                
                if jobs_found == 0:
                    print(f"\n⚠ No jobs found on page {page_num}. This might be the last page.")
                    # Continue to next page instead of breaking
                    # Some pages might be empty but later pages might have data
                    if page_num >= 3:  # If we hit 3 empty pages in a row, stop
                        print(f"⚠ Stopping as page appears empty.")
                        break
                
                # Small delay between pages to be polite to the server
                if page_num < max_pages:
                    time.sleep(2)
            
            print("\n" + "="*60)
            print(f"✅ SCRAPING COMPLETE!")
            print(f"Total pages scraped: {page_num}")
            print(f"Total jobs collected: {len(self.all_jobs)}")
            print("="*60)
            
            return self.all_jobs
            
        except Exception as e:
            print(f"\n❌ Error during scraping: {e}")
            import traceback
            traceback.print_exc()
            return self.all_jobs
        
        finally:
            self.driver.quit()
            print("\n🔒 Browser closed")

    def save_to_csv(self, filename='bdgovtjob_data.csv'):
        """Save scraped data to CSV"""
        if self.all_jobs:
            df = pd.DataFrame(self.all_jobs)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\n✅ CSV saved: {os.path.abspath(filename)}")
            print(f"   Rows: {len(self.all_jobs)}")
            return True
        else:
            print("\n⚠ No jobs to save to CSV")
            return False

    def save_to_json(self, filename='bdgovtjob_data.json'):
        """Save scraped data to JSON"""
        if self.all_jobs:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.all_jobs, f, ensure_ascii=False, indent=2)
            print(f"✅ JSON saved: {os.path.abspath(filename)}")
            print(f"   Records: {len(self.all_jobs)}")
            return True
        else:
            print("\n⚠ No jobs to save to JSON")
            return False
    
    def send_jobs_to_api(self, api_url):
        """Send scraped jobs to Django API"""
        if not self.all_jobs:
            print("\n⚠ No jobs to send to API")
            return False
        
        print(f"\n{'='*60}")
        print("📡 Sending data to API...")
        print(f"   API URL: {api_url}")
        print(f"   Jobs to send: {len(self.all_jobs)}")
        print('='*60)
        
        try:
            response = requests.post(
                api_url,
                json=self.all_jobs,
                headers={'Content-Type': 'application/json'},
                timeout=60
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"\n✅ API Response Success!")
                print(f"   Created: {result.get('total_created', 0)} jobs")
                print(f"   Updated: {result.get('total_updated', 0)} jobs")
                print(f"   Errors: {result.get('total_errors', 0)}")
                
                if result.get('errors'):
                    print(f"\n⚠ Some errors occurred:")
                    for error in result['errors'][:3]:  # Show first 3 errors
                        print(f"   - {error}")
                
                return True
            else:
                print(f"\n❌ API Error: HTTP {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
                
        except requests.exceptions.Timeout:
            print("\n❌ API request timed out (>60s)")
            print("   The server might be slow or unresponsive")
            return False
        except requests.exceptions.ConnectionError:
            print("\n❌ Cannot connect to API")
            print("   Make sure the Django server is running:")
            print("   cd bdjob_api_restframework/django-n8n-api")
            print("   python manage.py runserver")
            return False
        except Exception as e:
            print(f"\n❌ Failed to send to API: {e}")
            return False


def main():
    """Main function to run the scraper"""
    print("\n" + "🔷"*30)
    print("  BD GOVT JOB SCRAPER")
    print("  https://bdgovtjob.net")
    print("🔷"*30 + "\n")
    
    # Initialize scraper
    scraper = BDGovtJobScraper()
    
    # Scrape all pages (default: max 20 pages)
    # Change max_pages value to scrape more/less pages
    # Usage: MAX_PAGES=20 python bdgovtjob.py
    max_pages = int(os.environ.get('MAX_PAGES', 20))
    jobs = scraper.scrape_all_pages(max_pages=max_pages)
    
    if jobs:
        # Save to CSV
        scraper.save_to_csv(filename='bdgovtjob_data.csv')
        
        # Save to JSON
        scraper.save_to_json(filename='bdgovtjob_data.json')
        
        print("\n" + "="*60)
        print("🎉 SUCCESS! Data saved to:")
        print("   📄 bdgovtjob_data.csv")
        print("   📄 bdgovtjob_data.json")
        print("="*60)
        
        # Send to API (if API_URL is set)
        api_url = os.environ.get('API_URL', 'https://abdullah007ie.pythonanywhere.com/bdgovjob/send-data/')
        scraper.send_jobs_to_api(api_url)
        
        # Print summary statistics
        print("\n📊 SUMMARY:")
        print(f"   Total jobs: {len(jobs)}")
        
        # Count jobs with vacancies
        with_vacancies = sum(1 for job in jobs if job.get('vacancies') != 'N/A')
        total_vacancies = 0
        for job in jobs:
            vac = job.get('vacancies', '0')
            try:
                total_vacancies += int(vac) if vac != 'N/A' else 0
            except:
                pass
        
        print(f"   Jobs with vacancy info: {with_vacancies}")
        print(f"   Total vacancies: {total_vacancies}")
        
        # Show deadline distribution
        with_deadline = sum(1 for job in jobs if job.get('deadline') != 'N/A')
        print(f"   Jobs with deadline: {with_deadline}")
        
    else:
        print("\n❌ No jobs were scraped. Please check the website and try again.")
    
    print("\n✅ Scraper finished!\n")


if __name__ == "__main__":
    # Check if running with custom max pages
    # Usage: MAX_PAGES=5 python bdgovtjob.py
    main()

