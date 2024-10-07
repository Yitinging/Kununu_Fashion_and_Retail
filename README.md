Project Overview

This repository contains various analyses and web scraping projects focused on competitive analysis, employee attrition, and job posting data. The data has been sourced from multiple companies like Hugo Boss, LVMH, Adidas, Porsche, and Ralph Lauren. The repository is organized into different folders, each representing a specific analysis or data processing task.

Folder and File Descriptions

1. Code for First Presentation
Contains the initial code used for preparing the first presentation of the project.
Used for demonstrating initial insights and analysis using basic data processing techniques.

2. NLP with Kununu Data
Implements Natural Language Processing (NLP) to analyze employee reviews from Kununu.
Key tasks include text preprocessing, sentiment analysis, and extracting key topics from employee feedback.

3. Web Scrape Data from Job Postings
Scripts and data files related to web scraping job postings from various company websites.
Data extracted includes job titles, locations, functions, and additional insights (e.g., company descriptions).

4. Posting Frequency Analysis
Analyzes the frequency and distribution of job postings over time.
Used to identify hiring trends, peak posting times, and department-level demands.

5. Regression Analysis
Contains regression models applied to various datasets to understand the relationships between job postings, employee movement, and company performance.
Focused on predicting attrition and identifying key variables impacting employee retention.

6. Hugo_Boss_Attrition.csv
Contains data related to employee attrition at Hugo Boss.
surctria part focuses on specific criteria or attributes used in the analysis, such as department, function, and employee ratings.

7. Hugo_Boss_Attrition_by_function.csv
Similar to the Hugo_Boss_Attrition.csv, but grouped by specific functions (e.g., marketing, sales) to identify function-specific attrition trends.

8. company_benefits.ipynb
Analysis of company benefits across different organizations.
Data is merged and classified to provide insights on what benefits employees value most.

9. competitors_analysis.ipynb
Comparative analysis of competitors using extracted data from various sources.
Identifies strengths, weaknesses, and employee movement patterns between competing companies.

How to Use

Set Up Environment:
Clone the repository and install the required Python libraries listed in the requirements.txt file.
Set up the necessary drivers (e.g., ChromeDriver) if using Selenium for web scraping.

Run the Scripts:
Navigate to the specific folder and run the .ipynb or .py files as needed.
Each folder’s content is designed to be self-contained, and dependencies are specified within each script.

Review the Outputs:
CSV files and notebooks provide detailed outputs and visualizations.
Modify the scripts as needed to extract data from new sources or update the analyses.