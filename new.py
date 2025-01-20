
from bs4 import BeautifulSoup
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# Define the URL for the job listing page


def get_jobs(): 
    joblist=[]
    page=0
    while page <=0:

        url = f'https://www.mycareersfuture.gov.sg/search?sortBy=relevancy&page={page}'

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)  # Make sure you have the ChromeDriver installed
        driver.get(url)

        html_content = driver.page_source
        driver.quit()

        # Parse the content of the page
        soup = BeautifulSoup(html_content, 'html.parser')
        jobs=soup.find_all(attrs={"data-testid": "job-card-link"})
        ids = [job.get('href') for job in jobs]
        for i in ids:joblist.append(i)
        page+=1
    return joblist
# Function to fetch job details from the page
def get_job_details(joblist):
    for i in joblist:
        
        url = f'https://www.mycareersfuture.gov.sg{i}'
        print(url)
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)  # Make sure you have the ChromeDriver installed
        driver.get(url)

        html_content = driver.page_source
        driver.quit()
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
        save_job_to_csv(job_details)

    return job_details

# Function to save job details to CSV
def save_job_to_csv(job_details, filename='job_listing.csv'):
    fieldnames = ['Job Title', 'Company Name', 'Location', 'Categorie','Job type','Seniority','Minimum experience','Salary','Job Description', 'Job URL']

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only once
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(job_details)



# Main function to run the crawler
def crawl_job():

    a=get_jobs()
    
    # Get job details 
    get_job_details(a)
    

# Start the crawler
if __name__ == '__main__':
    crawl_job()
