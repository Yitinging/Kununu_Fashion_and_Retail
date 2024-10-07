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

# Get page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find the first job listing and extract its link
first_job = soup.find('li', class_='listSingleColumnItem')
job_link = first_job.find('a')['href'] if first_job.find('a') else 'No Link'
job_link = "https://careers.ralphlauren.com" + job_link if not job_link.startswith('https') else job_link

# Navigate to the job details page
driver.get(job_link)
time.sleep(5)  # Wait for the page to load completely

# Parse the job details page
job_details_soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract detailed job information
def extract_all_fields(soup):
    """Extract all fields from the job detail page and return them as a dictionary."""
    fields = {}
    
    # Extract job title
    job_title = soup.find('h2', class_='pageTitle').text.strip() if soup.find('h2', class_='pageTitle') else 'No Title'
    fields['Job Title'] = job_title
    
    # Extract all text content from fieldSet divs
    field_sets = soup.find_all('div', class_='fieldSet')
    job_description = ""
    
    for field in field_sets:
        # Extract the raw text content from each fieldSet div and concatenate it into a single job description
        field_text = field.text.strip() if field.text else ''
        if field_text:
            job_description += field_text + "\n"  # Add a newline for better readability

    # Add the entire job description to the fields dictionary
    fields['Job Description'] = job_description.strip()  # Remove leading/trailing newlines or spaces
    
    return fields

# Extract all fields and store them together
job_details = extract_all_fields(job_details_soup)

# Add the job link to the extracted fields
job_details['Job Link'] = job_link

# Convert the dictionary to a DataFrame and save to CSV
job_data = pd.DataFrame([job_details])  # Create a single-row DataFrame
csv_filename = 'ralph_lauren_job_details_fieldSet.csv'
job_data.to_csv(csv_filename, index=False)

print(f"Data extraction complete and saved to '{csv_filename}'")

# Close the WebDriver
driver.quit()
