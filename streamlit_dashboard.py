import streamlit as st
from job_scraper import JobScraper
from cover_letter_generator import generate_cover_letter
from email_sender import send_email
from google_sheets_integration import update_job_status_in_sheet

def display_dashboard():
    st.title("Job Scraping and Application Dashboard")
    scraper = JobScraper(["Software Engineer", "Data Scientist"], "NYC")
    scraper.fetch_jobs()
    jobs_df = scraper.get_saved_jobs()
    
    st.header("Available Job Listings")
    job_titles = jobs_df["job_title"].unique().tolist()
    selected_job_title = st.selectbox("Select a Job Title", job_titles)
    selected_job = jobs_df[jobs_df["job_title"] == selected_job_title].iloc[0]
    
    st.subheader("Job Details")
    st.write(f"**Company:** {selected_job['company']}")
    st.write(f"**Location:** {selected_job['location']}")
    st.write(f"**Salary Range:** {selected_job['salary_min']} - {selected_job['salary_max']}")
    st.write(f"**Job Description:** {selected_job['description']}")
    
    if st.button("Generate Cover Letter"):
        cover_letter = generate_cover_letter(selected_job["job_title"], selected_job["company"], selected_job["description"])
        st.text_area("Cover Letter", cover_letter, height=200)
        to_email = st.text_input("Enter Your Email Address")
        if st.button("Send Cover Letter"):
            if to_email:
                send_email(f"Application for {selected_job['job_title']} at {selected_job['company']}", cover_letter, to_email)
                update_job_status_in_sheet("your_spreadsheet_id", "Sheet1", selected_job.to_dict())
                st.success("Cover letter sent successfully!")
