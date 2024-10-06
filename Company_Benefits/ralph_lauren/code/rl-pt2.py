from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = "https://careers.ralphlauren.com/CareersCorporate/SearchJobsStore/?3413=9401&3413_format=1848&listFilterMode=1"
driver.get(url)

# Wait for the page to load
driver.implicitly_wait(10)

# Parse the main page to find all job links
soup = BeautifulSoup(driver.page_source, 'html.parser')
job_listings = soup.find_all('li', class_='listSingleColumnItem')  # Find all job listings

# Initialize an empty list to store all job details
all_job_details = []

# Loop through each job listing to extract its details
for job in job_listings:
    try:
        # Extract the link to the job detail page
        job_link = job.find('a')['href'] if job.find('a') else 'No Link'
        job_link = "https://careers.ralphlauren.com" + job_link if not job_link.startswith('https') else job_link

        # Navigate to the job details page
        driver.get(job_link)
        time.sleep(5)  # Wait for the page to load completely

        # Parse the job details page
        job_details_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract detailed job information
        job_details = {}
        
        # Extract job title
        job_title = job_details_soup.find('h2', class_='pageTitle').text.strip() if job_details_soup.find('h2', class_='pageTitle') else 'No Title'
        job_details['Job Title'] = job_title
        
        # Extract all text content from fieldSet divs for job description
        field_sets = job_details_soup.find_all('div', class_='fieldSet')
        job_description = ""
        
        for field in field_sets:
            # Extract the raw text content from each fieldSet div and concatenate it into a single job description
            field_text = field.text.strip() if field.text else ''
            if field_text:
                job_description += field_text + "\n"  # Add a newline for better readability

        # Add the entire job description to the fields dictionary
        job_details['Job Description'] = job_description.strip()  # Remove leading/trailing newlines or spaces
        
        # Add the job link to the extracted fields
        job_details['Job Link'] = job_link

        # Append the extracted job details to the list
        all_job_details.append(job_details)

        # Print confirmation of successful extraction
        print(f"Successfully extracted details for: {job_title}")

    except Exception as e:
        print(f"Error processing job listing: {e}")
        continue

# Convert the list of dictionaries to a DataFrame and save to CSV
job_data = pd.DataFrame(all_job_details)
csv_filename = 'ralph_lauren_all_jobs_details.csv'
job_data.to_csv(csv_filename, index=False)

print(f"Data extraction for all jobs complete and saved to '{csv_filename}'")

# Close the WebDriver
driver.quit()
