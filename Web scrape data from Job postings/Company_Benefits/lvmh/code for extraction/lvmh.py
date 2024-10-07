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

# Define an empty DataFrame to store the data
job_data_full = pd.DataFrame(columns=['Job Title', 'Location', 'Contract Type', 'Minimum Experience', 'Link', 'Job Responsibilities', 'Profile', 'Additional Information'])

# Function to handle overlays or pop-ups like cookie consent
def handle_popups():
    try:
        # Try to click on the "Reject All" or "Accept" button of a cookie consent if visible
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
        )
        cookie_button.click()
        print("Cookie consent dismissed.")
    except Exception as e:
        print("No cookie consent to dismiss or error handling it:", e)

# Function to extract data from each job
def extract_job_details(link):
    driver.get(link)
    time.sleep(2)  # Wait for page to load
    job_soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract job responsibilities, profile, and additional information if present
    job_responsibilities = job_soup.find('div', {'id': 'jobResponsabilities'}).text.strip() if job_soup.find('div', {'id': 'jobResponsabilities'}) else 'Not Available'
    profile = job_soup.find('div', {'id': 'profile'}).text.strip() if job_soup.find('div', {'id': 'profile'}) else 'Not Available'
    additional_info = job_soup.find('div', {'id': 'additionalInformation'}).text.strip() if job_soup.find('div', {'id': 'additionalInformation'}) else 'Not Available'

    return job_responsibilities, profile, additional_info

# Function to click on a specific page number using JavaScript if Selenium fails
def go_to_page(page_number):
    try:
        # Find the page number button using its text and click it
        page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, str(page_number)))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", page_button)  # Scroll to the page button
        time.sleep(1)  # Ensure it’s in view
        page_button.click()  # Attempt click
        print(f"Clicked on page {page_number}.")
        time.sleep(5)  # Wait for the page to load
        return True
    except Exception as e:
        print(f"Selenium click failed for page {page_number}: {e}")

        # Attempt JavaScript click as a fallback
        try:
            driver.execute_script("arguments[0].click();", page_button)
            print(f"JavaScript click successful on page {page_number}.")
            time.sleep(5)  # Wait for the page to load
            return True
        except Exception as js_error:
            print(f"JavaScript click also failed for page {page_number}: {js_error}")
            return False

# Loop through the pages and extract job information
page_number = 1
max_pages = 13  # Set the total number of pages you want to navigate through

while page_number <= max_pages:
    print(f"Extracting data from page {page_number}...")

    # Handle any overlays or pop-ups (e.g., cookie consent)
    handle_popups()

    # Parse the current page's content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract job listings on the current page
    job_listings = soup.find_all('div', class_='flex flex-col gap-2 text-center sm:text-left')
    
    for job in job_listings:
        try:
            # Extract job details like title, location, contract type, and experience
            job_title = job.find('h3').text.strip() if job.find('h3') else 'No Title'
            location = job.find_all('p')[0].text.strip() if len(job.find_all('p')) > 0 else 'No Location'
            contract_type = job.find_all('p')[1].text.strip() if len(job.find_all('p')) > 1 else 'No Contract Type'
            min_experience = job.find_all('p')[2].text.strip() if len(job.find_all('p')) > 2 else 'No Minimum Experience'
            
            # Extract the job link
            job_link = job.find('a', class_='flex')['href']
            job_link = "https://www.lvmh.com" + job_link if job_link else 'No Link'

            # Extract job responsibilities, profile, and additional information
            job_responsibilities, profile, additional_info = extract_job_details(job_link)

            # Create a temporary DataFrame for the current job
            temp_df = pd.DataFrame({
                'Job Title': [job_title],
                'Location': [location],
                'Contract Type': [contract_type],
                'Minimum Experience': [min_experience],
                'Link': [job_link],
                'Job Responsibilities': [job_responsibilities],
                'Profile': [profile],
                'Additional Information': [additional_info]
            })

            # Use pd.concat to add the new job data to the full DataFrame
            job_data_full = pd.concat([job_data_full, temp_df], ignore_index=True)
            
        except Exception as e:
            print(f"Error extracting data for job: {e}")
            continue

    # Navigate back to the main listings page URL after extracting all details from the current page
    driver.get(base_url)
    time.sleep(2)  # Wait for the main page to load again

    # Go to the next page number by clicking the number itself
    page_number += 1
    if not go_to_page(page_number):
        break

# Save the extracted data to a CSV file
driver.quit()
job_data_full.to_csv('lvmh_job_listings_complete.csv', index=False)
print("Data extraction complete and saved to 'lvmh_job_listings_complete.csv'")
