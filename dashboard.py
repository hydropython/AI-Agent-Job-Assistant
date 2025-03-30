import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import logging
from src.google_oauth import GoogleOAuth
import gspread

# Import functions from your existing files
from src.google_sheets_integration import authenticate_gsheet, update_job_status_in_sheet, get_job_status_from_sheet
from src.cover_letter_generator import generate_cover_letter, extract_experience_from_cv, extract_name_and_contact_from_cv, save_to_files
from src.email_sender import send_job_application_email
from src.job_scraper import JobScraper
from src.nlp_processing import extract_skills_from_description

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# --- Custom CSS for Styling ---
def load_css():
    st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            background-color: #4a90e2;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            border: none;
            font-weight: 500;
        }
        .stButton>button:hover {
            background-color: #357abd;
            color: white;
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border-radius: 8px;
            padding: 8px;
        }
        .stSelectbox>div>div>div {
            border-radius: 8px;
            padding: 4px;
        }
        .stDateInput>div>div>input {
            border-radius: 8px;
            padding: 8px;
        }
        .stNumberInput>div>div>input {
            border-radius: 8px;
            padding: 8px;
        }
        .header {
            color: #2c3e50;
            font-weight: 700;
        }
        .sidebar .sidebar-content {
            background-color: #2c3e50;
            color: white;
        }
        .sidebar .sidebar-content .stRadio>div {
            color: white;
        }
        .success-box {
            background-color: #d4edda;
            color: #155724;
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }
        .warning-box {
            background-color: #fff3cd;
            color: #856404;
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }
        .error-box {
            background-color: #f8d7da;
            color: #721c24;
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }
        .job-card {
            background-color: white;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .job-card h3 {
            color: #2c3e50;
            margin-top: 0;
        }
    </style>
    """, unsafe_allow_html=True)

# --- Streamlit UI Components ---
def main():
    st.set_page_config(
        page_title="AI Job Assistant",
        layout="wide",
        page_icon="💼"
    )
    load_css()
    
    # Sidebar navigation
    st.sidebar.title("💼 AI Job Assistant")
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Dashboard", "🔍 Job Search", "📝 Cover Letter", "✉️ Email Application", "📊 Application Tracker","⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    # st.sidebar.markdown("### Settings")
    # json_credentials_file = st.sidebar.text_input(
    #     "Google Sheets Credentials Path",
    #     "./Data/steam-bonbon-451912-d7-24cde95bb4e7.json",
    #     help="Path to your Google Sheets service account JSON file"
    # )
    # spreadsheet_id = st.sidebar.text_input(
    #     "Google Sheet ID",
    #     help="1Wcq6mmLmwWHHxtJN_B2RzZWSzRN-cfJkGjiLzDpm0ys"
    # )
    
    if page == "🏠 Dashboard":
        render_dashboard()
    elif page == "🔍 Job Search":
        render_job_search()
    elif page == "📝 Cover Letter":
        render_cover_letter_generator()
    elif page == "✉️ Email Application":
        render_email_application()
    elif page == "📊 Application Tracker":
        render_application_tracker()
        # render_application_tracker(json_credentials_file, spreadsheet_id)
    elif page == "⚙️ Settings":
        render_settings()  # Add this new condition

def render_dashboard():
    st.title("AI Job Assistant Dashboard")
    st.markdown("""
    Welcome to your AI-powered job application assistant! This tool helps you:
    
    - 🔍 Search for relevant job opportunities
    - 📝 Generate personalized cover letters
    - ✉️ Send professional application emails
    - 📊 Track your application progress
    
    Get started by selecting a page from the sidebar.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jobs Found", "25", "+5 from last week")
    with col2:
        st.metric("Applications Sent", "8", "3 pending")
    with col3:
        st.metric("Interview Rate", "25%", "2 of 8")
    
    st.markdown("---")
    st.subheader("Recent Activity")
    st.write("Your recent job application activity will appear here.")

def render_job_search():
    st.title("Job Search")
    st.markdown("Find your next career opportunity using our AI-powered job search.")
    
    with st.expander("🔍 Search Filters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            job_titles = st.text_input(
                "Job Titles (comma separated)",
                "Data Scientist, Machine Learning Engineer",
                help="Enter multiple job titles separated by commas"
            )
        with col2:
            location = st.text_input("Location", "London")
    
    if st.button("Search Jobs", key="search_jobs"):
        with st.spinner("🔍 Searching for jobs..."):
            job_list = [title.strip() for title in job_titles.split(",")]
            
            try:
                scraper = JobScraper(job_titles=job_list, location=location)
                scraper.scrape_jobs()
                jobs = scraper.get_saved_jobs()
                
                if not jobs.empty:
                    st.session_state.job_results = jobs
                    st.success(f"🎉 Found {len(jobs)} jobs!")
                    
                    # Display jobs in cards
                    for idx, job in jobs.iterrows():
                        with st.container():
                            st.markdown(f"""
                            <div class="job-card">
                                <h3>{job['job_title']}</h3>
                                <p><strong>Company:</strong> {job['company']}</p>
                                <p><strong>Location:</strong> {job['location']}</p>
                                <p><strong>Salary:</strong> £{job['salary_min']} - £{job['salary_max']}</p>
                                <a href="{job['apply_link']}" target="_blank">View Job</a>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("No jobs found. Try different search terms.")
            except Exception as e:
                st.error(f"Error searching for jobs: {str(e)}")

def render_cover_letter_generator():
    st.title("Cover Letter Generator")
    st.markdown("Create a personalized cover letter for your job application.")
    
    if 'job_results' in st.session_state and not st.session_state.job_results.empty:
        job_list = st.session_state.job_results[['job_title', 'company']].to_dict('records')
        job_options = {f"{job['job_title']} at {job['company']}": idx for idx, job in enumerate(job_list)}
        selected_job_key = st.selectbox(
            "Select a job to apply for",
            options=list(job_options.keys()),
            help="Select a job from your previous search results"
        )
        selected_job_idx = job_options[selected_job_key]
        selected_job = st.session_state.job_results.iloc[selected_job_idx]
        st.session_state.selected_job = selected_job
        
        with st.expander("📄 Job Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Job Title:** {selected_job['job_title']}")
                st.markdown(f"**Company:** {selected_job['company']}")
                st.markdown(f"**Location:** {selected_job['location']}")
            with col2:
                st.markdown(f"**Salary Range:** £{selected_job['salary_min']} - £{selected_job['salary_max']}")
                st.markdown(f"**Posted:** {selected_job['created']}")
                st.markdown(f"[Apply Here]({selected_job['apply_link']})")
            
            st.markdown("**Description:**")
            st.write(selected_job['description'][:500] + "...")
    else:
        st.warning("⚠️ No job results available. Please search for jobs first.")
        selected_job = None
    
    if selected_job is not None:
        st.subheader("Upload Your CV")
        cv_file = st.file_uploader(
            "Choose your CV file (PDF or DOCX)",
            type=['pdf', 'docx'],
            help="Upload your CV to personalize the cover letter"
        )
        
        if cv_file:
            # Save the uploaded file temporarily
            temp_cv_path = f"temp_cv.{cv_file.name.split('.')[-1]}"
            with open(temp_cv_path, "wb") as f:
                f.write(cv_file.getbuffer())
            
            st.session_state.cv_path = temp_cv_path
            st.success("✅ CV uploaded successfully!")
            
            if st.button("Generate Cover Letter", key="generate_cover_letter"):
                with st.spinner("✨ Generating your personalized cover letter..."):
                    try:
                        cover_letter = generate_cover_letter(
                            selected_job['job_title'],
                            selected_job['company'],
                            selected_job['description'],
                            temp_cv_path
                        )
                        st.session_state.cover_letter = cover_letter
                        
                        # Extract name from CV for saving files
                        name, _ = extract_name_and_contact_from_cv(temp_cv_path)
                        st.session_state.applicant_name = name
                        
                        st.subheader("Your Custom Cover Letter")
                        st.text_area(
                            "Cover Letter Content",
                            cover_letter,
                            height=400,
                            label_visibility="collapsed"
                        )
                        
                        # Save to files
                        if 'cover_letter_path' not in st.session_state:
                            cover_letter_path, _ = save_to_files(temp_cv_path, cover_letter, name)
                            st.session_state.cover_letter_path = cover_letter_path
                            st.session_state.cv_saved_path = temp_cv_path
                            st.success("📄 Cover letter saved successfully!")
                    except Exception as e:
                        st.error(f"Error generating cover letter: {str(e)}")

def render_email_application():
    st.title("Email Application")
    st.markdown("Send your job application with cover letter and CV attached.")
    
    if 'cover_letter' not in st.session_state or 'cv_path' not in st.session_state:
        st.warning("""
        ⚠️ Please complete these steps first:
        1. Search for jobs on the Job Search page
        2. Generate a cover letter on the Cover Letter page
        """)
        return
    
    with st.expander("✉️ Email Details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            recipient_email = st.text_input(
                "Recipient Email",
                help="The hiring manager's email address"
            )
        with col2:
            email_subject = st.text_input(
                "Subject",
                f"Application for {st.session_state.selected_job['job_title']} Position",
                help="Email subject line"
            )
    
    email_body = f"""
Dear Hiring Manager,

I hope this email finds you well. I am excited to apply for the {st.session_state.selected_job['job_title']} position at {st.session_state.selected_job['company']}. 
With my experience and skills, I am confident in my ability to contribute effectively to your team.

Please find my CV and cover letter attached for your review. I would appreciate the opportunity 
to discuss how my background aligns with the role. I look forward to your response.

Best regards,  
{st.session_state.applicant_name}
"""
    
    st.text_area(
        "Email Body",
        email_body,
        height=200,
        key="email_body"
    )
    
    if st.button("Send Application", key="send_application"):
        with st.spinner("📤 Sending your application..."):
            try:
                success = send_job_application_email(
                    recipient_email,
                    email_subject,
                    email_body,
                    st.session_state.cv_saved_path,
                    st.session_state.cover_letter_path
                )
                
                if success:
                    st.success("🎉 Application sent successfully!")
                    job_data = {  
                        "job_title": st.session_state.selected_job['job_title'],
                        "company": st.session_state.selected_job['company'],
                        "location": st.session_state.selected_job['location'],
                        "created": datetime.now().strftime("%Y-%m-%d"),
                        "salary_min": st.session_state.selected_job.get('salary_min', ''),
                        "salary_max": st.session_state.selected_job.get('salary_max', ''),
                        "apply_link": st.session_state.selected_job.get('apply_link', ''),
                        "status": "Applied",
                        "application_date": datetime.now().strftime("%Y-%m-%d"),
                        "interview_date": "",
                        "notes": "Application sent via AI Job Assistant"
                    }
                    
                    if update_job_status_in_sheet(
                        spreadsheet_id=st.session_state.spreadsheet_id,  # From session state
                        sheet_name="Sheet1",                              # Default or configurable
                        job_data=job_data                                 # The application data
                    ):
                        st.success("📊 Application status updated in tracker!")
                    else:
                        st.warning("Could not update application tracker.")
            except Exception as e:
                st.error(f"Error sending application: {str(e)}")

# def render_application_tracker(json_credentials_file, spreadsheet_id):
#     st.title("Application Tracker")
#     st.markdown("Track your job applications and their status.")
    
#     if not os.path.exists(json_credentials_file):
#         st.warning(f"⚠️ Google Sheets credentials file not found at {json_credentials_file}")
#         return
    
#     if not spreadsheet_id:
#         st.warning("Please enter a Google Sheet ID in the sidebar settings")
#         return
    
#     st.session_state.json_credentials_file = json_credentials_file
#     st.session_state.spreadsheet_id = spreadsheet_id
    
#     tab1, tab2 = st.tabs(["View Applications", "Add Application"])
    
#     with tab1:
#         st.subheader("Your Job Applications")
#         if st.button("Refresh Applications", key="refresh_apps"):
#             st.rerun()
        
#         applications = get_job_status_from_sheet(json_credentials_file, spreadsheet_id)
#         if applications:
#             df = pd.DataFrame(applications)
#             st.session_state.applications = df
            
#             # Status counts
#             status_counts = df['status'].value_counts().reset_index()
#             status_counts.columns = ['Status', 'Count']
            
#             col1, col2, col3 = st.columns([2, 3, 1])
#             with col1:
#                 st.dataframe(status_counts, hide_index=True)
#             with col2:
#                 st.bar_chart(status_counts.set_index('Status'))
            
#             st.dataframe(df)
#         else:
#             st.warning("No applications found or couldn't load data.")
    
#     with tab2:
#         st.subheader("Add New Application")
#         with st.form("new_application_form"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 job_title = st.text_input("Job Title*")
#                 company = st.text_input("Company*")
#                 location = st.text_input("Location")
#                 created = st.date_input("Date Posted", datetime.now())
#                 salary_min = st.number_input("Min Salary", min_value=0)
#             with col2:
#                 salary_max = st.number_input("Max Salary", min_value=0)
#                 apply_link = st.text_input("Application Link")
#                 status = st.selectbox(
#                     "Status*",
#                     ["Interested", "Applied", "Interview", "Offer", "Rejected"]
#                 )
#                 application_date = st.date_input("Application Date", datetime.now())
#                 interview_date = st.date_input("Interview Date", value=None)
            
#             notes = st.text_area("Notes")
            
#             submitted = st.form_submit_button("Add Application")
#             if submitted:
#                 if not job_title or not company or not status:
#                     st.error("Please fill in required fields (*)")
#                 else:
#                     job_data = {
#                         "job_title": job_title,
#                         "company": company,
#                         "location": location,
#                         "created": created.strftime("%Y-%m-%d"),
#                         "salary_min": salary_min,
#                         "salary_max": salary_max,
#                         "apply_link": apply_link,
#                         "status": status,
#                         "application_date": application_date.strftime("%Y-%m-%d"),
#                         "interview_date": interview_date.strftime("%Y-%m-%d") if interview_date else "",
#                         "notes": notes
#                     }
                    
#                     if update_job_status_in_sheet(
#                         json_credentials_file,
#                         spreadsheet_id,
#                         "Sheet1",
#                         job_data
#                     ):
#                         st.success("Application added successfully!")
#                         time.sleep(1)
#                         st.rerun()
#                     else:
#                         st.error("Failed to add application.")
def render_settings():
    st.title("Integration Settings")
    
    if 'gsheet_connected' not in st.session_state:
        st.session_state.gsheet_connected = False
    
    if not st.session_state.gsheet_connected:
        st.warning("Please connect your Google account")
        oauth = GoogleOAuth()
        creds = oauth.authenticate()  # This will trigger the auth flow
        
        if creds:
            st.session_state.gsheet_connected = True
            st.session_state.gsheet_creds = creds
            st.rerun()
    else:
        st.success("✅ Google Sheets connected")
        
        # Show sheet selection UI
        client = gspread.authorize(st.session_state.gsheet_creds)
        sheets = client.list_spreadsheet_files()
        
        if sheets:
            selected = st.selectbox(
                "Choose a spreadsheet",
                sheets,
                format_func=lambda x: x['name']
            )
            st.session_state.spreadsheet_id = selected['id']
            st.success(f"Selected: {selected['name']}")
        else:
            st.warning("No spreadsheets found in this account")
        
        if st.button("Disconnect"):
            del st.session_state.gsheet_connected
            del st.session_state.gsheet_creds
            if 'spreadsheet_id' in st.session_state:
                del st.session_state.spreadsheet_id
            st.rerun()

def render_application_tracker():
    st.title("Application Tracker")
    
    if 'gsheet_connected' not in st.session_state:
        st.warning("Please connect Google Sheets in Settings")
        return
    
    if 'spreadsheet_id' not in st.session_state:
        st.warning("Please select a spreadsheet in Settings")
        return
    
    tab1, tab2 = st.tabs(["View Applications", "Add Application"])
    
    with tab1:
        st.subheader("Your Job Applications")
        if st.button("Refresh Applications", key="refresh_apps"):
            st.rerun()
        try:
            # applications = get_job_status_from_sheet(st.session_state.spreadsheet_id)
            applications = get_job_status_from_sheet(
                spreadsheet_id=st.session_state.spreadsheet_id,
                sheet_name="Sheet1"  # or your preferred sheet name
            )
            if applications:
                df = pd.DataFrame(applications)
                st.session_state.applications = df
                
                # Status counts
                status_counts = df['status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                
                col1, col2, col3 = st.columns([2, 3, 1])
                with col1:
                    st.dataframe(status_counts, hide_index=True)
                with col2:
                    st.bar_chart(status_counts.set_index('Status'))
                
                st.dataframe(df)
            else:
                st.warning("No applications found or couldn't load data.")
        except Exception as e:
            st.error(f"Failed to load applications: {str(e)}")

    
    with tab2:
        st.subheader("Add New Application")
        with st.form("new_application_form"):
            col1, col2 = st.columns(2)
            with col1:
                job_title = st.text_input("Job Title*")
                company = st.text_input("Company*")
                location = st.text_input("Location")
                created = st.date_input("Date Posted", datetime.now())
                salary_min = st.number_input("Min Salary", min_value=0)
            with col2:
                salary_max = st.number_input("Max Salary", min_value=0)
                apply_link = st.text_input("Application Link")
                status = st.selectbox(
                    "Status*",
                    ["Interested", "Applied", "Interview", "Offer", "Rejected"]
                )
                application_date = st.date_input("Application Date", datetime.now())
                interview_date = st.date_input("Interview Date", value=None)
            
            notes = st.text_area("Notes")
            
            submitted = st.form_submit_button("Add Application")
            if submitted:
                if not job_title or not company or not status:
                    st.error("Please fill in required fields (*)")
                else:
                    job_data = {
                        "job_title": job_title,
                        "company": company,
                        "location": location,
                        "created": created.strftime("%Y-%m-%d"),
                        "salary_min": salary_min,
                        "salary_max": salary_max,
                        "apply_link": apply_link,
                        "status": status,
                        "application_date": application_date.strftime("%Y-%m-%d"),
                        "interview_date": interview_date.strftime("%Y-%m-%d") if interview_date else "",
                        "notes": notes
                    }
                    
                    if update_job_status_in_sheet(
                        st.session_state.spreadsheet_id,
                        "Sheet1",
                        job_data
                    ):
                        st.success("Application added successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Failed to add application.")

if __name__ == "__main__":
    main()