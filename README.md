
# AI Job Application Automation

This project is an intelligent job application automation system designed to streamline the job search process by scraping job listings, generating personalized cover letters, sending automated emails, and tracking job applications in a Google Sheets dashboard.

## Project Overview

The **AI Job Application Automation** project provides a fully automated solution for job seekers. It scrapes job listings from multiple job boards, processes the job data, generates personalized cover letters, sends automated emails with attachments, and tracks application statuses in a Google Sheets dashboard. This system helps users stay organized throughout their job application process and ensures timely follow-ups.

## Features

- **Job Scraping**: Automatically scrapes job listings from adzuna.com based on predefined search queries.
- **Cover Letter Generation**: Creates personalized cover letters based on the job title, company, job description, and experience extracted from uploaded CVs.
- **Email Sending**: Sends emails with the generated cover letters and uploaded CVs to the relevant job applications.
- **Job Tracking Dashboard**: Tracks job application status in a Google Sheets dashboard for easy reference.
- **Flask Dashboard**: Provides a real-time, interactive web dashboard for tracking job application statuses.

## Technologies Used

- **Python 3.x**: The primary programming language for the automation logic.
- **Flask**: A micro web framework used to build the web dashboard.

For more details on the required libraries, refer to the `requirements.txt` file.

## Project Structure

The project is organized into the following directories and modules:

### Root Structure:
```plaintext
AI-Job-Application-Automation/
├── config/                      # Configuration files (e.g., .env, SMTP settings)
├── database/                    # Database-related files (e.g., job application records)
├── env/                         # Virtual environment folder (excluded from Git)
├── src/                         # Source code for core modules
│   ├── job_scraper.py           # Scrapes job listings from job boards
│   ├── nlp_processing.py        # Processes job descriptions and generates personalized content
│   ├── cover_letter_generator.py# Generates cover letters based on scraped job data
│   ├── email_sender.py          # Sends emails with cover letters and attachments to job applications
│   ├── Google_sheet_integration.py# Provides a real-time dashboard to track job application statuses using Flask
├── static/                      # Static files (CSS, JS, images)
├── templates/                   # HTML templates for the Flask web app
├── uploads/                     # Uploaded files (e.g., resumes, job data)
├── __pycache__/                 # Python bytecode (auto-generated)
├── .gitignore                   # Files to be ignored by Git
├── LICENSE                      # License for your project
├── README.md                    # Project info and instructions
└── requirements.txt             # Python dependencies
```

## Setup & Installation

### Prerequisites
Ensure you have the following tools installed:

- **Python 3.x**: The primary programming language for the project.
- **pip**: Python package manager.


### Step 1: Clone the Repository

1. Open **VS Code**.
2. Open the terminal in VS Code by navigating to **Terminal > New Terminal**.
3. Clone the repository by running:

    ````bash
    [git clone https://github.com/hydropython/AI-Job-Application-Automation.git]
    cd AI-Job-Application-Automation
   ```

---

###  Step 2: Install Dependencies

Install the required Python libraries by running:

   ```bash
   pip install -r requirements.txt
   ```

This will install all necessary libraries, including **BeautifulSoup, gspread, Streamlit, pandas**, and others required for the project.

---

## Step 3: Set Up Google Sheets API

1. Go to the **Google Developers Console**.
2. Create a **new project** and enable the **Google Sheets API**.
3. Generate **service account credentials** in JSON format and download the file.
4. Save the credentials file in the **root directory** of the project.

---

## Step 4: Configure Email Settings

1. Set up an **SMTP email provider** (e.g., Gmail).
2. Update the `email_sender.py` script with your SMTP server details and email credentials.

---

## Usage

### Running the Automation

Once the setup is complete, start the automation process by running:

   ```bash
   python app.py
   ```

This will:

✅ Scrape job listings  
✅ Generate personalized cover letters  
✅ Send emails automatically  
✅ Track job application statuses in **Google Sheets**  

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Citations
The detail report https://app.readytensor.ai/publications/create/a0TkAcBrpkX1/documentation
