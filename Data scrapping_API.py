import requests
import pandas as pd
import sqlite3
import time
from datetime import datetime

class JobScraper:
    def __init__(self, app_id, app_key, job_titles, location="London", db_name="jobs.db"):
        self.app_id = app_id
        self.app_key = app_key
        self.job_titles = job_titles
        self.location = location
        self.url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()
    
    def create_table(self):
        """Creates the jobs table in SQLite if it doesn't exist."""
        query = '''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT,
            title TEXT,
            company TEXT,
            location TEXT,
            created TEXT,
            description TEXT,
            salary_min REAL,
            salary_max REAL,
            contract_type TEXT,
            contract_time TEXT,
            apply_link TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()
    
    def fetch_jobs(self):
        """Fetches job listings from Adzuna API and stores them in the database."""
        all_jobs = []
        
        for job_title in self.job_titles:
            params = {
                "app_id": self.app_id,
                "app_key": self.app_key,
                "what": job_title,
                "where": self.location,
                "results_per_page": 10
            }
            
            retries = 3
            for attempt in range(retries):
                response = requests.get(self.url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    jobs = data.get("results", [])
                    
                    if jobs:
                        for job in jobs:
                            all_jobs.append({
                                "job_title": job_title,
                                "title": job.get("title", "Unknown"),
                                "company": job.get("company", {}).get("display_name", "Unknown"),
                                "location": job.get("location", {}).get("display_name", "Unknown"),
                                "created": job.get("created", "Unknown"),
                                "description": job.get("description", "Unknown"),
                                "salary_min": job.get("salary_min", None),
                                "salary_max": job.get("salary_max", None),
                                "contract_type": job.get("contract_type", "Unknown"),
                                "contract_time": job.get("contract_time", "Unknown"),
                                "apply_link": job.get("redirect_url", "Unknown")
                            })
                        print(f"✅ Data for {job_title} added.")
                    else:
                        print(f"❌ No job data returned for {job_title}.")
                    break
                else:
                    print(f"⚠️ Error fetching data for {job_title}: {response.status_code}")
                    if attempt < retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        print("❌ Failed after multiple attempts.")
        
        if all_jobs:
            self.save_to_db(all_jobs)
            print("✅ Data saved to database.")
        else:
            print("❌ No job data to save.")
    
    def save_to_db(self, jobs):
        """Saves job data to SQLite database."""
        df = pd.DataFrame(jobs)
        df.to_sql("jobs", self.conn, if_exists="append", index=False)
    
    def get_saved_jobs(self):
        """Retrieves saved jobs from the database."""
        return pd.read_sql("SELECT * FROM jobs", self.conn)

if __name__ == "__main__":
    app_id = "aa0fe70e"
    app_key = "8f263064fae7759f6dabd1303edf8faf"
    job_titles = ["Data Scientist", "Software Engineer", "Machine Learning Engineer", "AI Researcher", "DevOps Engineer"]
    location = "London"

    scraper = JobScraper(app_id, app_key, job_titles, location)
    scraper.fetch_jobs()
    print(scraper.get_saved_jobs())
saved_jobs.to_csv("./Data/saved_jobs.csv", index=False)
print("✅ Data exported to saved_jobs.csv")