from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize the browser
driver = webdriver.Chrome()
url = "https://careers.hugoboss.com/global/en/search-results?keywords=&p=ChIJa76xwh5ymkcRW-WRjmtd6HU&location=Germany&latitude=50.1020951&longitude=8.6376017"
driver.get(url)

# Function to handle overlays or pop-ups like cookie consent and chatbot
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

    try:
        # Try to locate and close the chatbot window if visible
        chatbot_close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "PhenomChatbotWindowHeaderCloseButton"))
        )
        chatbot_close_button.click()
        print("Chatbot closed.")
    except Exception as e:
        print("No chatbot to close or error handling it:", e)

# Function to extract job details from a given job element by index
def extract_job_details(job_index):
    try:
        # Re-identify job elements to avoid stale element reference
        job_elements = driver.find_elements(By.CSS_SELECTOR, "div.information")

        # Select the job element based on its index
        job_element = job_elements[job_index]

        # Extract the job title from the given job element
        job_title = job_element.find_element(By.CSS_SELECTOR, "div.job-title").text.strip()

        # Extract all job-related information from the <p> element with class 'job-info'
        job_info = job_element.find_element(By.CSS_SELECTOR, "p.job-info").text.strip()

        # Extract the href link for detailed job information
        job_link_element = job_element.find_element(By.CSS_SELECTOR, "a[href*='job']")
        job_link = job_link_element.get_attribute("href").strip() if job_link_element else 'Link not found'
        print(f"Job Details Link: {job_link}")

        # Navigate to the job details page and extract more information
        driver.get(job_link)
        time.sleep(3)  # Wait for the page to load

        # Extract additional job details using the specific div class 'jd-info au-target'
        job_details_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.jd-info.au-target"))
        )
        job_details = job_details_element.text.strip() if job_details_element else 'No details available'

        # Return extracted details along with additional info
        return job_title, job_info, job_details
    except Exception as e:
        print(f"Error extracting job details: {e}")
        return None, None, None

# Function to click the back arrow icon to return to the main page
def click_back_arrow():
    try:
        # Locate and click the back arrow icon to return to the previous page
        back_arrow = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "i.icon.icon-left-arrow"))
        )
        back_arrow.click()
        print("Navigated back to the main page using the back arrow.")
    except Exception as e:
        print(f"Error clicking back arrow: {e}")

# Function to click the 'Next' button and move to the next page
def click_next_button():
    try:
        # Locate and click the 'Next' button to go to the next page
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.next-btn.au-target"))
        )
        next_button.click()
        print("Navigated to the next page.")
        time.sleep(5)  # Wait for the page to load
        return True
    except Exception as e:
        print(f"No more pages or error clicking next button: {e}")
        return False

# Handle any overlays or pop-ups
handle_popups()

# Initialize a list to hold all job details
all_job_details = []

# Track the page number for debugging
page_number = 1

# Extract details from the first page and continue through pagination
while True:
    print(f"Processing page {page_number}...")

    # Extract details for each job listing on the current page
    total_jobs = len(driver.find_elements(By.CSS_SELECTOR, "div.information"))  # Total job elements count

    for index in range(total_jobs):
        print(f"Processing job {index + 1}/{total_jobs} on page {page_number}...")

        # Extract details for the current job listing using its index
        job_title, job_info, job_details = extract_job_details(index)

        if job_title:  # If extraction was successful, add it to the list
            job_data = {
                'Job Title': job_title,
                'Job Info': job_info,
                'Job Details': job_details
            }
            all_job_details.append(job_data)

        # Return to the main search results page by clicking the back arrow
        click_back_arrow()
        time.sleep(3)  # Wait for the page to reload

    # Click the 'Next' button to navigate to the next page
    if not click_next_button():
        break  # Exit loop if no more pages are available

    page_number += 1

# Create a DataFrame from the collected job details
all_jobs_df = pd.DataFrame(all_job_details)

# Save the DataFrame to a CSV file
all_jobs_df.to_csv('all_hugo_boss_job_details.csv', index=False)
print("Data saved successfully to 'all_hugo_boss_job_details.csv'")

# Close the browser
driver.quit()
