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
driver.maximize_window()  # Maximize the window for better visibility

# Initialize an empty DataFrame to store job data
job_data_page_9 = pd.DataFrame(columns=['Job Title', 'Location', 'Link', 'Job Responsibilities', 'Profile', 'Additional Information'])

# Function to dismiss cookie consent popup
def handle_popups():
    try:
        cookie_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler")))
        cookie_button.click()
        print("Cookie consent dismissed.")
    except Exception as e:
        print(f"No cookie consent to dismiss or error handling it: {e}")

# Function to extract data from a single job's detail page
def extract_job_details(link):
    driver.get(link)
    time.sleep(2)  # Wait for page to load
    job_soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract job responsibilities, profile, and additional information if present
    job_responsibilities = job_soup.find('div', {'id': 'jobResponsabilities'}).text.strip() if job_soup.find('div', {'id': 'jobResponsabilities'}) else 'Not Available'
    profile = job_soup.find('div', {'id': 'profile'}).text.strip() if job_soup.find('div', {'id': 'profile'}) else 'Not Available'
    additional_info = job_soup.find('div', {'id': 'additionalInformation'}).text.strip() if job_soup.find('div', {'id': 'additionalInformation'}) else 'Not Available'

    return job_responsibilities, profile, additional_info

# Function to extract data from all jobs listed on the current page
def extract_jobs_from_page():
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_elements = soup.find_all('div', class_='flex flex-col gap-2 text-center sm:text-left')
        print(f"Found {len(job_elements)} job postings on this page.")

        for index, job_element in enumerate(job_elements):
            try:
                title = job_element.find('h3').text.strip()
                location = job_element.find('span', class_='ais-Highlight-nonHighlighted').text.strip() if job_element.find('span', class_='ais-Highlight-nonHighlighted') else 'Not Available'
                link_element = job_element.find('a', class_='flex')
                link = f"https://www.lvmh.com{link_element['href']}" if link_element else 'Not Available'

                print(f"Extracted Job {index + 1}: Title = {title}, Location = {location}, Link = {link}")  # Debug information

                # Extract additional details from the job link
                job_responsibilities, profile, additional_info = extract_job_details(link)

                # Add to the DataFrame
                job_data_page_9.loc[len(job_data_page_9)] = [title, location, link, job_responsibilities, profile, additional_info]
            
            except Exception as e:
                print(f"Error extracting job data: {e}")
                continue
    except Exception as e:
        print(f"Failed to extract jobs from the page: {e}")

# Function to navigate to a specific page using JavaScript
def navigate_to_page_9():
    try:
        # First, go to page 7
        page_7_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Page 7']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", page_7_button)
        page_7_button.click()
        print("Navigated to page 7.")
        time.sleep(5)  # Wait for the page to load

        # Now, go to page 8
        page_8_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Page 8']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", page_8_button)
        page_8_button.click()
        print("Navigated to page 8.")
        time.sleep(5)  # Wait for the page to load

        # Now, go to page 9
        page_9_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Page 9']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", page_9_button)
        page_9_button.click()
        print("Navigated to page 9.")
        time.sleep(5)  # Wait for the page to load
    except Exception as e:
        print(f"Failed to navigate to page 9: {e}")

# Start the process
handle_popups()

# Navigate to page 9
navigate_to_page_9()

# Extract job postings from page 9
print("Extracting jobs from page 9...")
extract_jobs_from_page()

# Save the data to a CSV file
job_data_page_9.to_csv('lvmh_job_listings_page_9_with_details.csv', index=False)
print("Data extraction from page 9 complete and saved to 'lvmh_job_listings_page_9_with_details.csv'.")
driver.quit()
