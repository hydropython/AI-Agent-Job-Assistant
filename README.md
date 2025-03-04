
# AI Job Application Automation

This project is an intelligent job application automation system designed to streamline the job search process by scraping job listings, generating personalized cover letters, sending automated emails, and tracking job applications in a Google Sheets dashboard.


## Project Overview

The **AI Job Application Automation** project provides a fully automated solution for job seekers. It scrapes job listings from multiple job boards, processes the job data, generates personalized cover letters, sends automated emails with attachments, and tracks application statuses in a Google Sheets dashboard. This system helps users stay organized throughout their job application process and ensures timely follow-ups.

## Features

- **Job Scraping**: Automatically scrapes job listings from adzuna.com based on predefined search queries.
- **Cover Letter Generation**: Creates personalized cover letters based on the job title, company,job description, and experiance extracted from uploded CV.
- **Email Sending**: Sends emails with the generated cover letters and uploded CV to the relevant job applications.
- **Job Tracking Dashboard**: Tracks job application status in a Google Sheets dashboard for easy reference.
- **Streamlit Dashboard**: Provides a real-time, interactive web dashboard for tracking job application statuses.

## Technologies Used

- **Python 3.x**: The primary programming language for the automation logic.
- **BeautifulSoup**: Web scraping library to parse HTML and extract job listing data.
- **NLP (Natural Language Processing)**: Used for processing job data and generating personalized content.
- **gspread**: For interacting with Google Sheets to track job application statuses.
- **Streamlit**: A framework to build the interactive dashboard.
- **smtplib & email**: For sending cover letters and CV via email.
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

1. Open **VS Code**.
2. Open the terminal in VS Code by navigating to **Terminal > New Terminal**.
3. Clone the repository by running:

    ````bash
    git clone https://github.com/yourusername/AI-Job-Application-Automation.git
    cd AI-Job-Application-Automation
    ````

## Step 1: Clone the Repository

1. Open **VS Code**.
2. Open the terminal by navigating to **Terminal > New Terminal**.
3. Clone the repository and navigate into the project folder:

   ```bash
   git clone https://github.com/hydropython/AI-Job-Application-Automation.git
   cd AI-Job-Application-Automation
   ```

---

## Step 2: Install Dependencies

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
   python run.py
   ```

This will:

✅ Scrape job listings  
✅ Generate personalized cover letters  
✅ Send emails automatically  
✅ Track job application statuses in **Google Sheets**  

---

## Running the Streamlit Dashboard

To launch the Streamlit dashboard, run:

   ```bash
   streamlit run dashboard.py
   ```

This will start the web-based dashboard for monitoring job applications.

---

## Contributing

Feel free to contribute by submitting issues or pull requests. Make sure to follow best practices and test your changes before pushing.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
