import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import logging

logging.basicConfig(level=logging.INFO)

# Function to authenticate Google Sheets using Service Account
def authenticate_gsheet(json_credentials_file):
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(json_credentials_file, scopes=scopes)
    
    # Refresh the credentials if they are expired
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    
    # Authorize the client and return the gspread client
    client = gspread.authorize(creds)
    return client

# Function to update job application status in Google Sheets
def update_job_status_in_sheet(spreadsheet_id, sheet_name, job_data):
    try:
        # Authenticate and get the Google Sheets client
        client = authenticate_gsheet("./Data/job-followup-e2ca373e066a.json")
        
        # Open the Google Sheet using its ID and get the specified worksheet
        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        
        # Prepare the job data to append as a new row
        job_row = [
            job_data["job_title"], job_data["company"], job_data["location"], job_data["created"],
            job_data["salary_min"], job_data["salary_max"], job_data["apply_link"], 
            job_data["status"], job_data["application_date"], job_data["interview_date"], job_data["notes"]
        ]
        
        # Append the job data row to the sheet
        sheet.append_row(job_row)
        logging.info(f"Job data for {job_data['job_title']} added to Google Sheets.")
    except Exception as e:
        logging.error(f"Error updating Google Sheets: {e}")

# Example usage of the function:
job_data = {
    "job_title": "Data Scientist",
    "company": "Tech Corp",
    "location": "New York",
    "created": "2025-03-01",
    "salary_min": "100000",
    "salary_max": "150000",
    "apply_link": "https://example.com/apply",
    "status": "Applied",  # Can be "Applied", "Interviewing", "Offer", "Rejected"
    "application_date": "2025-03-01",
    "interview_date": "2025-03-15",  # If applicable
    "notes": "First round interview scheduled."
}

# Replace with your Google Sheets ID and sheet name
spreadsheet_id = '106284332103486967563'
sheet_name = 'job_status'

update_job_status_in_sheet(spreadsheet_id, sheet_name, job_data)