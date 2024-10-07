from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Initialize the browser
driver = webdriver.Chrome()
base_url = "https://www.lvmh.com/en/join-us/our-job-offers?PRD-en-us-timestamp-desc%5BrefinementList%5D%5BgeographicAreaFilter%5D%5B0%5D=Europe&PRD-en-us-timestamp-desc%5BrefinementList%5D%5BcountryRegionFilter%5D%5B0%5D=Germany"
driver.get(base_url)
driver.maximize_window()

# Initialize an empty DataFrame to store job data
job_data_page_13_complete = pd.DataFrame(columns=['Job Title', 'Location', 'Link', 'Job Responsibilities', 'Profile', 'Additional Information'])

# Function to handle popups like cookie consent
def handle_popups():
    try:
        cookie_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler")))
        cookie_button.click()
    except Exception as e:
        print(f"Cookie consent not found or already dismissed: {e}")

# Function to extract data from a single job's detail page
def extract_job_details(link):
    try:
        driver.get(link)
        time.sleep(4)  # Wait for the page to fully load
        job_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract job details
        job_responsibilities = job_soup.find('div', {'id': 'jobResponsabilities'}).text.strip() if job_soup.find('div', {'id': 'jobResponsabilities'}) else 'Not Available'
        profile = job_soup.find('div', {'id': 'profile'}).text.strip() if job_soup.find('div', {'id': 'profile'}) else 'Not Available'
        additional_info = job_soup.find('div', {'id': 'additionalInformation'}).text.strip() if job_soup.find('div', {'id': 'additionalInformation'}) else 'Not Available'
        
        return job_responsibilities, profile, additional_info
    except Exception as e:
        print(f"Error extracting job details for link {link}: {e}")
        return 'Not Available', 'Not Available', 'Not Available'

# Navigate directly to page 13
def navigate_to_page_13():
    try:
        # Click directly on page 13 link
        page_13_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='13']")))
        page_13_button.click()
        time.sleep(4)  # Wait for the page to load

        print("Successfully navigated to page 13.")
    except Exception as e:
        print(f"Failed to navigate to page 13: {e}")

# Extract job data from page 13
def extract_jobs_from_page_13():
    try:
        # Navigate to page 13
        navigate_to_page_13()
        
        # Wait for the jobs on page 13 to load
        job_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/join-us/our-job-offers/')]")))

        for job_element in job_elements:
            try:
                job_title = job_element.text
                job_link = job_element.get_attribute('href')
                job_location = job_element.find_element(By.XPATH, ".//following-sibling::span").text if job_element.find_element(By.XPATH, ".//following-sibling::span") else 'Not Available'
                
                # Extract detailed information from the job link
                job_responsibilities, profile, additional_info = extract_job_details(job_link)

                # Append to the DataFrame
                job_data_page_13_complete.loc[len(job_data_page_13_complete)] = [job_title, job_location, job_link, job_responsibilities, profile, additional_info]
                print(f"Extracted details for job: {job_title}")

            except Exception as e:
                print(f"Error processing job element: {e}")

        print("Extraction from page 13 completed.")
    except Exception as e:
        print(f"Error extracting jobs from page 13: {e}")

# Run the extraction process for page 13
handle_popups()
extract_jobs_from_page_13()

# Save the data to a CSV file
job_data_page_13_complete.to_csv("page_13_job_data.csv", index=False)

# Close the browser
driver.quit()
