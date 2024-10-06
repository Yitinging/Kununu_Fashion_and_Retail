import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read the CSV file
file_path = 'adidas_jobs_complete.csv'  # Update with your file path
job_data_new = pd.read_csv(file_path)

# Step 2: Define English and German benefit keywords
english_benefit_keywords = {
    'Health and Insurance Benefits': ['health', 'insurance'],
    'Career Development Opportunities': ['career', 'development', 'training', 'growth', 'leadership'],
    'Paid Time Off / Vacation': ['vacation', 'paid time off'],
    'Company Culture and Work Environment': ['culture', 'work environment', 'flexible', 'work-life balance'],
    'Employee Discounts and Perks': ['discount', 'perks']
}

german_benefit_keywords = {
    'Health and Insurance Benefits': ['gesundheit', 'versicherung'],
    'Career Development Opportunities': ['karriere', 'entwicklung', 'training', 'wachstum', 'führung'],
    'Paid Time Off / Vacation': ['urlaub', 'freizeit'],
    'Company Culture and Work Environment': ['kultur', 'arbeitsumfeld', 'flexibel', 'work-life balance'],
    'Employee Discounts and Perks': ['rabatt', 'vorteil']
}

# Step 3: Define new standard categories (fixing the missing definition)
new_standard_categories = [
    'Health and Insurance Benefits', 
    'Career Development Opportunities', 
    'Paid Time Off / Vacation', 
    'Company Culture and Work Environment', 
    'Employee Discounts and Perks'
]

# Step 4: Initialize a list to store the classification results
combined_benefit_classifications = []

# Step 5: Analyze and classify benefits based on job descriptions for both languages
for index, row in job_data_new.iterrows():
    job_description = row['Job Description']
    job_title = row['Job Title']
    
    # Initialize a dictionary to store benefits for each job
    job_benefits = {'Job Title': job_title}
    
    # Check English keywords
    for category, keywords in english_benefit_keywords.items():
        job_benefits[category] = any(keyword in job_description.lower() for keyword in keywords)
    
    # Check German keywords
    for category, keywords in german_benefit_keywords.items():
        job_benefits[category] = job_benefits.get(category, False) or any(keyword in job_description.lower() for keyword in keywords)
    
    # Append the results to the classification list
    combined_benefit_classifications.append(job_benefits)

# Step 6: Convert the classification results into a DataFrame
classified_benefits_combined_df = pd.DataFrame(combined_benefit_classifications)

# Step 7: Calculate the percentage of each benefit category
combined_benefit_counts = classified_benefits_combined_df[new_standard_categories].sum()

# Step 8: Plot the percentage of each benefit category
plt.figure(figsize=(10, 6))
plt.bar(combined_benefit_counts.index, (combined_benefit_counts / len(classified_benefits_combined_df)) * 100)

# Add title and labels
plt.title('Percentage of Jobs Offering Each Benefit Category (Combined Analysis)', fontsize=14)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xlabel('Benefit Category', fontsize=12)

# Display percentage labels on the bars
for i, v in enumerate((combined_benefit_counts / len(classified_benefits_combined_df)) * 100):
    plt.text(i, v + 1, f'{v:.1f}%', ha='center', fontsize=12)

plt.show()

# Step 9: Save the classified results to a new CSV file
output_file_path_combined = 'adidas_jobs_benefits_classified_combined_1.csv'  # Update with your desired output path
classified_benefits_combined_df.to_csv(output_file_path_combined, index=False)

# Output the path of the saved file
print(f"Classified benefits saved to: {output_file_path_combined}")
