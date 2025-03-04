
# AI Job Application Automation

This project is an intelligent job application automation system designed to streamline the job search process by scraping job listings, generating personalized cover letters, sending automated emails, and tracking job applications in a Google Sheets dashboard.


## Project Overview

The **AI Job Application Automation** project provides a fully automated solution for job seekers. It scrapes job listings from multiple job boards, processes the job data, generates personalized cover letters, sends automated emails with attachments, and tracks application statuses in a Google Sheets dashboard. This system helps users stay organized throughout their job application process and ensures timely follow-ups.

## Features

- **Job Scraping**: Automatically scrapes job listings from popular job boards based on predefined search queries.
- **Cover Letter Generation**: Creates personalized cover letters based on the job title, company, and job description.
- **Email Sending**: Sends emails with the generated cover letters to the relevant job applications.
- **Job Tracking Dashboard**: Tracks job application status in a Google Sheets dashboard for easy reference.
- **Streamlit Dashboard**: Provides a real-time, interactive web dashboard for tracking job application statuses.

## Technologies Used

- **Python 3.x**: The primary programming language for the automation logic.
- **BeautifulSoup**: Web scraping library to parse HTML and extract job listing data.
- **NLP (Natural Language Processing)**: Used for processing job data and generating personalized content.
- **gspread**: For interacting with Google Sheets to track job application statuses.
- **Streamlit**: A framework to build the interactive dashboard.
- **smtplib & email**: For sending cover letters via email.
- **pandas**: For handling data manipulation and storing job listings.

## Project Structure

The project is organized into the following Python modules:

- **job_scraper.py**: Scrapes job listings from job boards.
- **nlp_processing.py**: Processes job descriptions and generates personalized content.
- **cover_letter_generator.py**: Generates cover letters based on scraped job data.
- **email_sender.py**: Sends emails with cover letters and attachments to job applications.
- **streamlit_dashboard.py**: Provides a real-time dashboard to track job application statuses.
- **run.py**: The main script that runs the job application automation process.

## Setup & Installation

### Prerequisites
Ensure you have the following tools installed:

- **Visual Studio Code (VS Code)**: The recommended code editor.
- **Python 3.x**: The primary programming language for the project.
- **pip**: Python package manager.
- **Google Cloud Project**: A Google Cloud Project with Sheets API enabled and service account credentials (.json file) downloaded.

### Step 1: Clone the Repository

Open **VS Code**.

Open the terminal in VS Code by navigating to **Terminal > New Terminal**.

Clone the repository by running:

```bash
git clone https://github.com/yourusername/AI-Job-Application-Automation.git
cd AI-Job-Application-Automation

### Step 2: Install Dependencies

Install the required Python libraries by running the following command:

```bash
pip install -r requirements.txt

