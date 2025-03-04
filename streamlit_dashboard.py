import streamlit as st
from job_scraper import JobScraper  # Ensure this is correct based on your class name
from cover_letter_generator import generate_cover_letter
from email_sender import send_email
from google_sheets_integration import update_job_status_in_sheet
from datetime import datetime
import pytz

def add_bg_image(image_path):
    # CSS to add a background image to the Streamlit app
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_path});  # Replace with correct path if needed
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def display_dashboard():
    # Set background image
    add_bg_image('https://your-image-url.com')  # Replace with a valid image URL or local path
    
    st.title("Job Scraping and Application Dashboard")
    
    # Add a subheader with a company logo or decorative image
    st.image('https://your-logo-url.com', width=150)  # Replace with a logo or attractive image

    # Custom styles for the dashboard
    st.markdown("""<style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;  # Green color for the title
        }
        .header {
            font-size: 28px;
            color: #F1C40F;  # Gold color for header
        }
        .subheader {
            font-size: 24px;
            color: #1F618D;  # Blue color for subheader
        }
        .job-details {
            background-color: rgba(255, 255, 255, 0.8);  # Light background for job details
            padding: 20px;
            border-radius: 10px;
            margin-top: 10px;
        }
        .job-info {
            margin-bottom: 10px;
        }
        .btn {
            background-color: #4CAF50;  # Green button
            color: white;
            border-radius: 5px;
            padding: 10px;
            text-align: center;
            font-size: 16px;
            width: 100%;
        }
        .btn:hover {
            background-color: #45a049;
        }
    </style>""", unsafe_allow_html=True)

    # Create an instance of the JobScraperAPI class
    app_id = '####'  # Replace with your app ID
    api_key = '####'
    scraper = JobScraper(app_id, api_key, ["Software Engineer", "Data Scientist"], "NYC")
    
    # Fetch jobs using the scraper
    scraper.fetch_jobs()
    jobs_df = scraper.get_saved_jobs()

    if jobs_df.empty:
        st.warning("No job listings found.")
        return

    st.header("Available Job Listings")
    job_titles = jobs_df["job_title"].unique().tolist()
    selected_job_title = st.selectbox("Select a Job Title", job_titles)
    
    if selected_job_title:
        selected_job = jobs_df[jobs_df["job_title"] == selected_job_title].iloc[0]
        
        # Job Details Section
        st.markdown('<div class="job-details">', unsafe_allow_html=True)

        st.subheader(f"**Company:** {selected_job['company']}")
        st.markdown(f"**Location:** {selected_job['location']}", unsafe_allow_html=True)
        
        # Posting Date - Convert to timezone-aware datetime
        posting_date = selected_job['created']  # Adjust to the correct column name if different
        posting_date = datetime.strptime(posting_date, "%Y-%m-%dT%H:%M:%S%z")  # Adjust the format if necessary
        now = datetime.now(pytz.utc)  # Make sure to use timezone-aware datetime
        days_ago = (now - posting_date).days
        st.markdown(f"**Posting Date:** {posting_date.strftime('%Y-%m-%d')} ({days_ago} days ago)", unsafe_allow_html=True)

        st.markdown(f"**Description:** {selected_job['description']}", unsafe_allow_html=True)
        st.markdown(f"**Salary Range:** {selected_job['salary_min']} - {selected_job['salary_max']}", unsafe_allow_html=True)
        st.markdown(f"**Contract Type:** {selected_job['contract_type']}", unsafe_allow_html=True)
        st.markdown(f"**Contract Time:** {selected_job['contract_time']}", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Add tabs using st.radio
        tab = st.radio("Select an Action", ("Upload CV", "Generate Cover Letter"))

        if tab == "Upload CV":
            # Upload CV functionality
            uploaded_cv = st.file_uploader("Upload Your CV", type=["pdf", "doc", "docx"])
            
            # Store the uploaded CV in session state
            if uploaded_cv is not None:
                st.session_state.uploaded_cv = uploaded_cv
                st.write(f"**Uploaded CV:** {uploaded_cv.name}")
                st.success("CV uploaded successfully!")
            else:
                if "uploaded_cv" in st.session_state:
                    uploaded_cv = st.session_state.uploaded_cv
                    st.write(f"**Uploaded CV:** {uploaded_cv.name}")

        if tab == "Generate Cover Letter":
            # Generate Cover Letter functionality
            try:
                if "uploaded_cv" in st.session_state:
                    uploaded_cv = st.session_state.uploaded_cv
                    
                    # Ensure to pass the uploaded CV to the generate_cover_letter function
                    cover_letter = generate_cover_letter(
                        selected_job["job_title"], 
                        selected_job["company"], 
                        selected_job["description"],
                        uploaded_cv
                    )
                    st.text_area("Cover Letter", cover_letter, height=200)
                
                    to_email = st.text_input("Enter Your Email Address")
                    if st.button("Send Cover Letter"):
                        if to_email:
                            send_email(f"Application for {selected_job['job_title']} at {selected_job['company']}", cover_letter, to_email)
                            update_job_status_in_sheet("your_spreadsheet_id", "Sheet1", selected_job.to_dict())
                            st.success("Cover letter sent successfully!")
                        else:
                            st.error("Please enter a valid email address.")
                else:
                    st.error("Please upload a CV before generating a cover letter.")
            except Exception as e:
                st.error(f"Error generating or sending cover letter: {str(e)}")