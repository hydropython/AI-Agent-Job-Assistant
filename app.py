from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from werkzeug.utils import secure_filename
import pandas as pd
from src.job_scraper import JobScraper  # Import the JobScraper class from job_scraper.py
from src.cover_letter_generator import generate_cover_letter  # Import cover letter generator function
from dotenv import load_dotenv
from src.orchestrator import run_automation  # NEW: Import orchestrator
from email_sender import send_job_application_email  # NEW: Import

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv(dotenv_path='app.env')

# Get API key and secret key from environment variables
API_KEY = os.getenv('API_KEY')
APP_ID = os.getenv('APP_ID')
SECRET_KEY = os.getenv('SECRET_KEY')  # Load SECRET_KEY from the environment

# Set the secret key for sessions and security
app.secret_key = SECRET_KEY  # This is required for Flask sessions

# Define the folder where you want to save uploaded CVs
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    # NEW: Run automation on homepage load and display results
    jobs = []
    agent_status = "Idle"
    try:
        result = run_automation()  # NEW: Call orchestrator
        if isinstance(result, list):  # Assuming orchestrator returns a list of jobs
            jobs = result
            agent_status = "Scraper: Done, Writer: Done, Tracker: Done"  # NEW: Static status for now
        else:
            flash('No jobs found or automation failed.', 'error')
    except Exception as e:
        flash(f'Error running automation: {e}', 'error')
    return render_template('index.html', jobs=jobs, agent_status=agent_status)  # NEW: Pass jobs and status
    # return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    job_title = request.form['job_title']
    location = request.form['location']
    
    # Initialize the JobScraper without passing API_KEY (it's already in the .env file)
    scraper = JobScraper(job_titles=[job_title], location=location)
    scraper.scrape_jobs()
    
    saved_jobs = scraper.get_saved_jobs()
    
    if isinstance(saved_jobs, pd.DataFrame) and not saved_jobs.empty:
        # NEW: Convert DataFrame to list of dicts for template
        jobs = saved_jobs.to_dict(orient="records")
        agent_status = "Scraper: Done"  # NEW: Simple status for scrape route
        # return render_template('result.html', jobs=saved_jobs.to_dict(orient="records"))
        return render_template('result.html', jobs=jobs, agent_status=agent_status)  # NEW: Pass status
    else:
        return render_template('no_jobs_found.html')

# @app.route('/apply_job', methods=['GET', 'POST'])
# def apply_job():
#     job_url = request.args.get('job_url')  # Get job URL from query parameters
    
#     if request.method == 'POST':
#         cover_letter = request.form.get('cover_letter')
#         if cover_letter:
#             # Generate cover letter using the uploaded CV and the passed job info
#             job_title = request.form['job_title']
#             company = request.form['company']
#             job_desc = request.form['job_desc']
#             cover_letter_text = generate_cover_letter(job_title, company, job_desc, None)  # CV path can be handled separately
     
#             # Generate cover letter (optional: use user-provided cover letter)
#             cv_path = "uploads/Tihetna_Mesfin  - CV.pdf"  # Replace with actual CV path from upload
#             applicant_name = "Your Name"  # Replace with extracted name
#             cover_letter_text = generate_cover_letter(job_title, company, job_desc, cv_path)
#             if cover_letter:
#                 cover_letter_text = cover_letter
            
#             # Send email
#             send_job_application_email(
#                 to_email=["recruiter1@example.com", "recruiter2@example.com"],  # Multiple recipients
#                 job_title=job_title,
#                 company=company,
#                 applicant_name=applicant_name,
#                 cv_path=cv_path
#             )
            
#             # Save or email the cover letter here if needed
#             flash('Cover letter submitted successfully!', 'success')
#             return redirect(url_for('index'))
#         else:
#             flash('Please write a cover letter before submitting.', 'error')

#     return render_template('upload.html', job_url=job_url)  # Pass job URL to the template

@app.route('/upload_cv', methods=['GET', 'POST'])
def upload_cv():
    cover_letter = None  # Initialize to None
    
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'cv' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        cv = request.files['cv']
        
        if cv.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if cv and allowed_file(cv.filename):
            filename = secure_filename(cv.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            cv.save(file_path)
            
            # Get job details from the form
            job_title = request.form['job_title']
            company = request.form['company']
            job_desc = request.form['job_desc']
            
            # Generate the cover letter using the function
            cover_letter = generate_cover_letter(job_title, company, job_desc, file_path)

            flash('Cover letter generated successfully!', 'success')
        else:
            flash('Allowed file types are pdf, docx, and txt', 'error')
            return redirect(request.url)
    
    return render_template('upload.html', cover_letter=cover_letter)  # Pass cover letter to template

if __name__ == '__main__':
    app.run(debug=True)