import csv
import os
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from config import constants as CONSTANTS


class Scraper():
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        # Define the URL for the job listing page
        chrome_install = ChromeDriverManager().install()

        folder = os.path.dirname(chrome_install)
        chromedriver_path = os.path.join(folder, "chromedriver.exe")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path),options=options)
    def get_jobs(self, driver): 
        page=0
        while page <=499:
            joblist=[]
            print("Crawling Page",page)
            url = f'https://www.mycareersfuture.gov.sg/search?sortBy=relevancy&page={page}'

            driver.get(url)
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "job-card-0")))
                html_content = driver.page_source
                # Parse the content of the page
                soup = BeautifulSoup(html_content, 'html.parser')
                jobs=soup.find_all(attrs={"data-testid": "job-card-link"})
                ids = [job.get('href') for job in jobs]
                for i in ids:joblist.append(i)
                self.get_job_details(driver,joblist)
            except:
                pass
            page+=1
    # Function to fetch job details from the page
    def get_job_details(self, driver,joblist):
        for i in joblist:
            
            url = f'https://www.mycareersfuture.gov.sg{i}'
            print(url)
            driver.get(url)
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="description-content"]/descendant::p')))
                html_content = driver.page_source
                # Parse the content of the page
                soup = BeautifulSoup(html_content, 'html.parser')
                # Extract job details
                job_title = soup.find(attrs={"data-testid": "job-details-info-job-title"}).text.strip() if soup.find(attrs={"data-testid": "job-details-info-job-title"}) else 'N/A'
                company_name = soup.find(attrs={"data-testid": "company-hire-info"}).text.strip() if soup.find(attrs={"data-testid": "company-hire-info"}) else 'N/A'
                location = soup.find(attrs={"data-testid": "job-details-info-location-map"}).text.strip() if soup.find(attrs={"data-testid": "job-details-info-location-map"}) else 'N/A'
                categorie=soup.find(attrs={"data-testid": "job-details-info-job-categories"}).text.strip() if soup.find(attrs={"data-testid": "job-details-info-job-categories"}) else 'N/A'
                jobtype=soup.find(attrs={"data-testid": "job-details-info-employment-type"}).text.strip() if soup.find(attrs={"data-testid": "job-details-info-employment-type"}) else 'N/A'
                seniority=soup.find(attrs={"data-testid": "job-details-info-seniority"}).text.strip() if soup.find(attrs={"data-testid": "job-details-info-seniority"}) else 'N/A'
                minexp=soup.find(attrs={"data-testid": "job-details-info-min-experience"}).text.strip() if soup.find(attrs={"data-testid": "job-details-info-min-experience"}) else 'N/A'
                salary=soup.find(attrs={"data-testid": "salary-range"}).text.strip() if soup.find(attrs={"data-testid": "salary-range"}) else 'N/A'
                job_description = soup.find(attrs={"data-testid": "description-content"}).text.strip() if soup.find(attrs={"data-testid": "description-content"}) else 'N/A'
                job_description=job_description.replace("\n", " ")
                # Return a dictionary with job details
                job_details = {
                    'Job Title': job_title,
                    'Company Name': company_name,
                    'Location': location,
                    'Categorie':categorie,
                    'Job type':jobtype,
                    'Seniority':seniority,
                    'Minimum experience':minexp,
                    'Salary':salary,
                    'Job Description': job_description,
                    'Job URL': url
                }
                self.save_job_to_csv(job_details)
            except:
                pass


    # Function to save job details to CSV
    def save_job_to_csv(self, job_details):
        fieldnames = ['Job Title', 'Company Name', 'Location', 'Categorie','Job type','Seniority','Minimum experience','Salary','Job Description', 'Job URL']
        filename=Path(__file__).parent.parent / f'datasets/{CONSTANTS.SCRAPE_OUTPUT_FILE}'
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write header only once
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(job_details)



    # Main function to run the crawler
    def scrape(self):
        self.get_jobs(self.driver)
        self.driver.quit()
