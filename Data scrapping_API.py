import requests
import pandas as pd
from datetime import datetime
import time

# Your API credentials
app_id = "aa0fe70e"
app_key = "8f263064fae7759f6dabd1303edf8faf"

# API URL
url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

# List of job titles in computer science
job_titles = ["Data Scientist", "Software Engineer", "Machine Learning Engineer", "AI Researcher", "DevOps Engineer"]

# Create an empty DataFrame to store all results
all_jobs_df = pd.DataFrame()

# Loop through the job titles and make API requests
for job_title in job_titles:
    # Parameters for job search
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": job_title,
        "where": "London",
        "results_per_page": 10
    }

    # Make API request
    response = requests.get(url, params=params)

    # Check response
    if response.status_code == 200:
        data = response.json()

        # Extract job listings
        jobs = data.get("results", [])

        if jobs:
            # Convert to DataFrame
            df = pd.DataFrame(jobs)

            # Extract clean company names
            df["company"] = df["company"].apply(lambda x: x.get("display_name", "Unknown") if isinstance(x, dict) else "Unknown")

            # Add job title as a new column
            df["job_title"] = job_title

            # Select relevant columns, handling missing columns
            columns_to_select = ["job_title", "title", "company", "location", "created", "description", "salary_min", "salary_max", "contract_type", "contract_time"]

            # Check if columns exist in the DataFrame
            existing_columns = [col for col in columns_to_select if col in df.columns]
            
            # Select only the existing columns
            df = df[existing_columns]

            # Add row numbers
            df.insert(0, "No", range(1, len(df) + 1))

            # Append the current job results to the all_jobs_df
            all_jobs_df = pd.concat([all_jobs_df, df], ignore_index=True)

            print(f"✅ Data for {job_title} added.")
        else:
            print(f"❌ No job data returned for {job_title}.")
    else:
        print(f"❌ Error fetching data for {job_title}: {response.status_code}")
        print(response.text)

    # To avoid hitting rate limits, you can add a small delay
    time.sleep(2)

# Save all results to CSV
if not all_jobs_df.empty:
    all_jobs_df.to_csv("adzuna_computer_science_jobs.csv", index=False)
    print("✅ Data saved to adzuna_computer_science_jobs.csv")
else:
    print("❌ No job data to save.")