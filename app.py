from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
import pandas as pd
from src.job_scraper import JobScraper  # Import the JobScraper class from job_scraper.py
from cover_letter_generator import generate_cover_letter  # Import cover letter generator function
from dotenv import load_dotenv

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
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    job_title = request.form['job_title']
    location = request.form['location']
    
    # Initialize the JobScraper without passing API_KEY (it's already in the .env file)
    scraper = JobScraper(job_titles=[job_title], location=location)
    scraper.scrape_jobs()
    
    saved_jobs = scraper.get_saved_jobs()
    
    if isinstance(saved_jobs, pd.DataFrame) and not saved_jobs.empty:
        return render_template('result.html', jobs=saved_jobs.to_dict(orient="records"))
    else:
        return render_template('no_jobs_found.html')

@app.route('/apply_job', methods=['GET', 'POST'])
def apply_job():
    job_url = request.args.get('job_url')  # Get job URL from query parameters
    
    if request.method == 'POST':
        cover_letter = request.form.get('cover_letter')
        if cover_letter:
            # Generate cover letter using the uploaded CV and the passed job info
            job_title = request.form['job_title']
            company = request.form['company']
            job_desc = request.form['job_desc']
            cover_letter_text = generate_cover_letter(job_title, company, job_desc, None)  # CV path can be handled separately

            # Save or email the cover letter here if needed
            flash('Cover letter submitted successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Please write a cover letter before submitting.', 'error')

    return render_template('upload.html', job_url=job_url)  # Pass job URL to the template

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