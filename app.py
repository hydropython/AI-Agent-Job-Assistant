import os
from flask import Flask, request, redirect, url_for
from email_sender import send_email  # Assuming this function is implemented in email_sender.py
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the folder where the CV will be saved
UPLOAD_FOLDER = 'uploads'  # Folder to save uploaded CVs
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}  # Allowed file types for the CV

# Configure the Flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_cover_letter(job_title, company, job_description, cv_path):
    """
    Function to generate a personalized cover letter.
    In this example, it simply returns a static message, but it can be
    dynamically customized based on the job and company.
    """
    cover_letter = f"""
    Dear Hiring Manager,

    I am writing to express my interest in the {job_title} position at {company}. I am confident that my experience in
    {job_description} makes me a strong candidate for this role.

    Please find attached my CV for your consideration.

    I look forward to hearing from you.

    Best regards,
    [Your Name]
    """
    return cover_letter

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Ensure file is part of the form and is allowed
        file = request.files.get('cv')
        if file and allowed_file(file.filename):
            # Secure the file name and save the file to the server
            filename = secure_filename(file.filename)
            uploaded_cv_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploaded_cv_path)

            # Generate a cover letter based on the job information
            job_title = request.form['job_title']
            company = request.form['company']
            job_description = request.form['job_description']
            cover_letter = generate_cover_letter(job_title, company, job_description, uploaded_cv_path)

            # Retrieve email from the form and send email with the CV attached
            to_email = request.form['email']
            send_email(f"Application for {job_title} at {company}", cover_letter, to_email, uploaded_cv_path)

            return "Cover letter sent and CV uploaded successfully!"
        else:
            return "Invalid file format. Only PDF, DOC, DOCX files are allowed."

    # HTML form for uploading the CV and entering email
    return '''
    <!doctype html>
    <title>Upload CV</title>
    <h1>Upload your CV</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="cv" required><br><br>
      <input type="text" name="job_title" placeholder="Job Title" required><br><br>
      <input type="text" name="company" placeholder="Company Name" required><br><br>
      <textarea name="job_description" placeholder="Job Description" required></textarea><br><br>
      <input type="email" name="email" placeholder="Enter your email" required><br><br>
      <input type="submit" value="Submit">
    </form>
    '''

if __name__ == '__main__':
    # Ensure the uploads directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)

