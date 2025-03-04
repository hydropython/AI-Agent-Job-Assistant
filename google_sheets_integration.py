import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import logging

logging.basicConfig(level=logging.INFO)

def authenticate_gsheet(json_credentials_file):
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(json_credentials_file, scopes=scopes)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return gspread.authorize(creds)

def update_job_status_in_sheet(spreadsheet_id, sheet_name, job_data):
    client = authenticate_gsheet("credentials.json")
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
    job_row = [
        job_data["job_title"], job_data["company"], job_data["location"], job_data["created"],
        job_data["salary_min"], job_data["salary_max"], job_data["apply_link"], job_data["status"]
    ]
    sheet.append_row(job_row)
    logging.info(f"Job data for {job_data['job_title']} added to Google Sheets.")