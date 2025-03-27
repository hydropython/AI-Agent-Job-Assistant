from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
import pandas as pd
from job_scraper import JobScraper  # Import the JobScraper class from job_scraper.py
from cover_letter_generator import generate_cover_letter  # Import cover letter generator function

app = Flask(__name__)

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
    
    # Initialize the JobScraper and scrape jobs
    scraper = JobScraper(job_titles=[job_title], location=location)
    scraper.scrape_jobs()
    
    saved_jobs = scraper.get_saved_jobs()
    
    if isinstance(saved_jobs, pd.DataFrame) and not saved_jobs.empty:
        return render_template('result.html', jobs=saved_jobs.to_dict(orient="records"))
    else:
        return render_template('no_jobs_found.html')

@app.route('/apply_job/<job_url>', methods=['GET', 'POST'])
def apply_job(job_url):
    if request.method == 'POST':
        cover_letter = request.form.get('cover_letter')
        if cover_letter:
            # Process the cover letter (e.g., save to database, send email, etc.)
            flash('Cover letter submitted successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Please write a cover letter before submitting.', 'error')
    return render_template('apply_job.html', job_url=job_url)
