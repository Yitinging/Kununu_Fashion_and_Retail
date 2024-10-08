from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize the browser
driver = webdriver.Chrome()
url = "https://jobs.porsche.com/index.php?ac=search_result&search_criterion_country%5B%5D=46&search_criterion_channel%5B%5D=12"
driver.get(url)

# Function to handle pop-ups or initial page load delays if necessary
def handle_popups():
    try:
        # Wait for the page to load or handle any initial pop-ups
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.jb-dt-list-body tr")))  # Wait for the job listings to be visible
    except Exception as e:
        print("Error during initial page load or pop-up handling:", e)

# Function to extract details of a job posting and navigate to the detailed job page
def extract_job_details(job_index):
    try:
        # Re-identify job elements to avoid stale element reference
        job_elements = driver.find_elements(By.CSS_SELECTOR, "tbody.jb-dt-list-body tr")

        # Select the job element based on its index
        job_element = job_elements[job_index]

        # Extract the job title using the first <td> element within the row
        job_title = job_element.find_element(By.CSS_SELECTOR, "td.column-jobad-title").text.strip()

        # Extract the company name, location, and function using appropriate <td> elements
        company_name = job_element.find_element(By.XPATH, ".//td[@data-column-title='Gesellschaft']").text.strip()
        location = job_element.find_element(By.XPATH, ".//td[@data-column-title='Standort']").text.strip()
        function = job_element.find_element(By.XPATH, ".//td[@data-column-title='Funktion']").text.strip()

        # Extract the relative href link within the <a> tag and form the full URL
        relative_link = job_element.find_element(By.CSS_SELECTOR, "td.column-jobad-title a").get_attribute("href")
        if relative_link.startswith("index.php"):
            job_link = f"https://jobs.porsche.com/{relative_link}"  # Form the full URL by appending base URL
        else:
            job_link = relative_link  # Use as is if it's a complete link

        # Navigate to the job details page using the full job link
        driver.get(job_link)
        time.sleep(3)  # Wait for the page to load

        # Extract the detailed job description from the <div> element with class 'row'
        detailed_job_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.row"))
        )
        detailed_job_description = detailed_job_element.text.strip() if detailed_job_element else 'No details available'

        # Check for the presence of "Exklusive Einblicke hinter die Kulissen" section
        additional_info = ''
        try:
            # If the section is found, click on the plus icon and extract the additional information
            section_element = driver.find_element(By.XPATH, "//span[contains(text(),'Exklusive Einblicke hinter die Kulissen')]")
            toggle_icon = section_element.find_element(By.XPATH, "../../span[contains(@class, 'panel-toggle-icon')]")
            toggle_icon.click()  # Click the plus icon to expand the section
            time.sleep(2)  # Wait for the section to expand

            # Extract the additional information
            additional_info_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.panel-body"))
            )
            additional_info = additional_info_element.text.strip() if additional_info_element else 'No additional information available'
        except:
            additional_info = 'Section not found or could not extract additional information'

        # Return all extracted details as a dictionary
        return {
            'Job Title': job_title,
            'Company Name': company_name,
            'Location': location,
            'Function': function,
            'Job Link': job_link,
            'Detailed Job Description': detailed_job_description,
            'Additional Information': additional_info
        }
    except Exception as e:
        print(f"Error extracting job details for job {job_index + 1}: {e}")
        return None

# Handle any initial page load pop-ups
handle_popups()

# Wait for user to manually set the number of job postings to 250 and then confirm to continue
input("Please manually set the number of job postings to 250 on the webpage, then press Enter to continue...")

# Initialize a list to hold all job details
all_job_details = []

# Get the total number of job postings on the current page
total_jobs = len(driver.find_elements(By.CSS_SELECTOR, "tbody.jb-dt-list-body tr"))
print(f"Total job postings found: {total_jobs}")

# Extract details for each job listing
for index in range(total_jobs):
    job_details = extract_job_details(index)
    if job_details:
        all_job_details.append(job_details)

    # Navigate back to the main page to extract the next job
    driver.back()
    time.sleep(3)  # Wait for the page to reload

# Create a DataFrame from the collected job details
all_jobs_df = pd.DataFrame(all_job_details)

# Save the DataFrame to a CSV file
all_jobs_df.to_csv('all_porsche_job_details_with_additional_info.csv', index=False)

# Close the browser
driver.quit()
