import logging
import schedule
import time
import requests
from transformers import pipeline
import sqlite3
import pandas as pd
from datetime import datetime

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

# Initialize the text generation model
generator = pipeline("text-generation", model="gpt2")

# Job Scraper Class
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
                        logging.info(f"✅ Data for {job_title} added.")
                    else:
                        logging.warning(f"❌ No job data returned for {job_title}.")
                    break
                else:
                    logging.warning(f"⚠️ Error fetching data for {job_title}: {response.status_code}")
                    if attempt < retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        logging.error("❌ Failed after multiple attempts.")
        
        if all_jobs:
            self.save_to_db(all_jobs)
            logging.info("✅ Data saved to database.")
        else:
            logging.error("❌ No job data to save.")

    def save_to_db(self, jobs):
        """Saves job data to SQLite database."""
        df = pd.DataFrame(jobs)
        df.to_sql("jobs", self.conn, if_exists="append", index=False)
    
    def get_saved_jobs(self):
        """Retrieves saved jobs from the database."""
        return pd.read_sql("SELECT * FROM jobs", self.conn)

# Cover Letter Generation
def generate_cover_letter(job_title, company, job_desc, skills, max_new_tokens=300, temperature=0.7, top_p=0.9):
    """
    Generates a professional and personalized cover letter.
    """
    logging.info("Inside the generate_cover_letter function...")

    # Create a refined prompt with more context and a clean structure
    prompt = (
        f"Dear Hiring Manager,\n\n"
        f"I am excited to apply for the {job_title} position at {company}. With a strong background in "
        f"{', '.join(skills)}, I am eager to contribute my expertise to your team.\n\n"
        f"Job Description: {job_desc}\n\n"
        f"I believe my skills in {', '.join(skills)} make me an excellent fit for this role. I am particularly excited "
        f"about the opportunity to work with big data and apply machine learning techniques to drive business insights. "
        f"I look forward to the possibility of discussing how I can contribute to {company}.\n\n"
        f"Thank you for your consideration, and I am excited about the opportunity to further discuss my application."
    )

    logging.info(f"Prompt:\n{prompt}")

    try:
        response = generator(prompt, 
                             max_new_tokens=max_new_tokens, 
                             do_sample=True, 
                             temperature=temperature, 
                             top_p=top_p,
                             repetition_penalty=1.2)  # Reduces redundancy
        generated_text = response[0]['generated_text']
        logging.info("Generated text successfully.")
    except Exception as e:
        logging.error(f"Error generating text: {e}")
        return "Error generating cover letter."

    return generated_text


def job_fetching_and_cover_letter_generation():
    """
    Fetch jobs, scrape data, and generate cover letters.
    This is the task that will run periodically.
    """
    logging.info("Starting the job fetching and cover letter generation process...")

    # Initialize the scraper
    app_id = "aa0fe70e"
    app_key = "8f263064fae7759f6dabd1303edf8faf"
    job_titles = ["Data Scientist", "Software Engineer", "Machine Learning Engineer", "AI Researcher", "DevOps Engineer"]
    location = "London"
    scraper = JobScraper(app_id, app_key, job_titles, location)
    
    # Fetch jobs and save to the database
    scraper.fetch_jobs()

    # Fetch saved jobs and generate cover letters
    jobs_df = scraper.get_saved_jobs()

    for _, job in jobs_df.iterrows():
        job_title = job["job_title"]
        company = job["company"]
        job_desc = job["description"]
        skills = ["Python", "Machine Learning", "Data Analysis"]  # You can customize this per job
        cover_letter = generate_cover_letter(job_title, company, job_desc, skills)

        # Print the generated cover letter
        logging.info(f"\nGenerated Cover Letter for {job_title} at {company}:")
        print(cover_letter)


# Schedule the job to run every hour
schedule.every(1).hour.do(job_fetching_and_cover_letter_generation)

# Infinite loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # wait for 1 minute before checking again
