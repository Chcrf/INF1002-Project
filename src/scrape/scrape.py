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
    '''
    A module that scrapes the MyCareersFuture website
    '''
    def __init__(self):
        '''
        Create a chrome driver for scraping
        '''
        options = Options()
        options.add_argument("--headless")
        # Define the URL for the job listing page
        chrome_install = ChromeDriverManager().install()

        folder = os.path.dirname(chrome_install)
        chromedriver_path = os.path.join(folder, "chromedriver.exe")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path),options=options)

    def _get_jobs(self): 
        '''
        A private function that goes through individual job listing on the MyCareersFuture website
        '''
        page=0
        while page <=499:
            joblist=[]
            print("Crawling Page",page)
            url = f'https://www.mycareersfuture.gov.sg/search?sortBy=relevancy&page={page}'

            self.driver.get(url)
            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "job-card-0")))
                html_content = self.driver.page_source
                # Parse the content of the page
                soup = BeautifulSoup(html_content, 'html.parser')
                jobs=soup.find_all(attrs={"data-testid": "job-card-link"})
                ids = [job.get('href') for job in jobs]
                for i in ids:
                    joblist.append(i)
                self._get_job_details(joblist)
            except:
                pass
            page+=1
    # Function to fetch job details from the page
    def _get_job_details(self,joblist):
        '''
        A private function that extracts job details from individual job listings on the MyCareersFuture website

        Parameters:
            joblist (list): A list containing the link to the individual job listings
        '''
        for i in joblist:
            
            url = f'https://www.mycareersfuture.gov.sg{i}'
            print(url)
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="description-content"]/descendant::p')))
                html_content = self.driver.page_source
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
                self._save_job_to_csv(job_details)
            except:
                pass


    # Function to save job details to CSV
    def _save_job_to_csv(self, job_details):
        '''
        A private function that stores extracted data into a csv file

        Parameters:
            job_details (dict):  A dictionary that contains job details

        File Output:
            config/constants.py::SCRAPE_OUTPUT_FILE 
        '''
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
        '''
        Main function to start the scraper
        '''
        self._get_jobs()
        self.driver.quit()
