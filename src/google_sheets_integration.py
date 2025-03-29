import os
import time
import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import logging
import traceback
from crewai import Agent  # NEW: Import for crewAI
from dotenv import load_dotenv

# Load environment variables from google_sheets.env
load_dotenv("google_sheets.env")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Google Sheets authentication function
def authenticate_gsheet(json_credentials_file):
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(json_credentials_file, scopes=scopes)

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        return gspread.authorize(creds)
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        return None

# Function to update job application status in Google Sheets
def update_job_status_in_sheet(json_credentials_file, spreadsheet_id, sheet_name="Sheet1", job_data={}):
    try:
        client = authenticate_gsheet(json_credentials_file)
        if not client:
            return False

        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

        required_fields = ["job_title", "company", "status"]
        if not all(field in job_data for field in required_fields):
            logging.error("Missing required fields in job_data.")
            return False

        job_row = [
            job_data.get("job_title", ""), job_data.get("company", ""), job_data.get("location", ""),
            job_data.get("created", ""), job_data.get("salary_min", ""), job_data.get("salary_max", ""),
            job_data.get("apply_link", ""), job_data.get("status", ""), job_data.get("application_date", ""),
            job_data.get("interview_date", ""), job_data.get("notes", "")
        ]

        retries = 3
        for attempt in range(retries):
            try:
                sheet.append_row(job_row)
                logging.info(f"Job data for {job_data['job_title']} added to Google Sheets.")
                return True
            except gspread.exceptions.APIError as api_err:
                logging.error(f"API Error (attempt {attempt+1}/{retries}): {api_err}")
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                logging.error(f"Unexpected error updating Google Sheets: {e}")
                print(traceback.format_exc())
                return False

    except Exception as e:
        logging.error(f"Error in update_job_status_in_sheet: {e}")
        print(traceback.format_exc())

    return False

# Function to retrieve job application statuses from Google Sheets
# Function to retrieve job application statuses
def get_job_status_from_sheet(json_credentials_file, spreadsheet_id, sheet_name="job_status"):
    try:
        client = authenticate_gsheet(json_credentials_file)
        if not client:
            return None

        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

        # Define expected headers in the correct order and names
        expected_headers = [
            "job_title", "company", "location", "created", "salary_min", "salary_max",
            "apply_link", "status", "application_date", "interview_date", "notes"
        ]

        job_records = sheet.get_all_records(expected_headers=expected_headers)

        logging.info(f"Retrieved {len(job_records)} job application records.")
        return job_records

    except gspread.exceptions.APIError as api_err:
        logging.error(f"Google Sheets API Error: {api_err}")
    except Exception as e:
        logging.error(f"Error retrieving job status: {e}")

    return None

# NEW: Define Tracker Agent tool
def track_job_agent(job_data):
    json_credentials_file = os.getenv("GSHEET_CREDENTIALS", "./Data/steam-bonbon-451912-d7-24cde95bb4e7.json")
    spreadsheet_id = ''
    return update_job_status_in_sheet(json_credentials_file, spreadsheet_id, "Sheet1", job_data)

# NEW: Define Tracker Agent
tracker_agent = Agent(
    role="Status Tracker",
    goal="Log job applications in Google Sheets",
    backstory="Organized data manager",
    verbose=True,
    tools=[track_job_agent]
)
# Example usage
if __name__ == "__main__":
    # Set the credentials file and Google Sheet ID
    json_credentials_file = os.getenv("GSHEET_CREDENTIALS", "./Data/steam-bonbon-451912-d7-24cde95bb4e7.json")
    spreadsheet_id = ''  # Correct spreadsheet ID
    sheet_name = 'Sheet1'  # Update this if the sheet name is different (check your sheet's actual name)

    # Sample job application data
    job_data = {
        "job_title": "Data Scientist",
        "company": "Tech Corp",
        "location": "New York",
        "created": "2025-03-01",
        "salary_min": "100000",
        "salary_max": "150000",
        "apply_link": "https://example.com/apply",
        "status": "Applied",
        "application_date": "2025-03-01",
        "interview_date": "2025-03-15",
        "notes": "First round interview scheduled."
    }

    # Update job status in the sheet
    if update_job_status_in_sheet(json_credentials_file, spreadsheet_id, sheet_name, job_data):
        # Retrieve and print all job application records
        job_applications = get_job_status_from_sheet(json_credentials_file, spreadsheet_id, sheet_name)
        if job_applications:
            for job in job_applications:
                print(job)
