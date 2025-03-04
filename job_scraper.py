# job_scraper.py
import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

class JobScraper:
    def __init__(self, job_titles, location):
        self.job_titles = job_titles
        self.location = location
        self.saved_jobs = []

    def fetch_jobs(self):
        logging.info("Fetching jobs from job portal...")
        for job_title in self.job_titles:
            url = f"https://job-portal.com/search?q={job_title}&location={self.location}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            
            for job_listing in soup.find_all("div", class_="job-listing"):
                job = {
                    "job_title": job_title,
                    "company": job_listing.find("h3").text.strip(),
                    "description": job_listing.find("p", class_="job-desc").text.strip(),
                    "location": job_listing.find("span", class_="location").text.strip(),
                    "apply_link": job_listing.find("a", class_="apply-link")["href"],
                    "created": job_listing.find("span", class_="created").text.strip(),
                    "salary_min": job_listing.find("span", class_="salary-min").text.strip(),
                    "salary_max": job_listing.find("span", class_="salary-max").text.strip(),
                    "status": "Not Applied"
                }
                self.saved_jobs.append(job)

    def get_saved_jobs(self):
        return pd.DataFrame(self.saved_jobs)