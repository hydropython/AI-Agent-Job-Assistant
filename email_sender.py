import smtplib
import os
import time
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from cover_letter_generator import generate_cover_letter  # Import the cover letter generator

# Load environment variables from .env file
load_dotenv('email.env')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_job_application_email(to_email, job_title, company, applicant_name, cv_path):
    try:
        # Open the CV file and pass the file object
        with open(cv_path, 'rb') as cv_file:
            cover_letter_path = generate_cover_letter(job_title, company, applicant_name, cv_file)

        # Get email credentials from environment variables
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')
        email_host = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
        email_port = int(os.getenv('EMAIL_PORT', 587))

        if not email_user or not email_password:
            logging.error("Email credentials are not set properly in environment variables.")
            return

        # Define the email subject and body
        subject = f"Application for {job_title} Position at {company}"
        body = f"""
        Dear Hiring Manager,

        I hope this email finds you well. I am excited to apply for the {job_title} position at {company}. 
        With my experience and skills, I am confident in my ability to contribute effectively to your team.

        Please find my CV and cover letter attached for your review. I would appreciate the opportunity 
        to discuss how my background aligns with the role. I look forward to your response.

        Best regards,  
        {applicant_name}
        """

        # Log the start of the email sending process
        logging.info(f"Preparing to send email to {to_email}...")

        # Create message object
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = ", ".join(to_email) if isinstance(to_email, list) else to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach CV
        logging.info(f"Attaching CV from {cv_path}")
        with open(cv_path, 'rb') as cv_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(cv_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(cv_path)}')
            msg.attach(part)

        # Attach cover letter
        logging.info(f"Attaching cover letter from {cover_letter_path}")
        with open(cover_letter_path, 'rb') as cover_letter_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(cover_letter_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(cover_letter_path)}')
            msg.attach(part)

        retries = 3  # Number of retry attempts
        for attempt in range(retries):
            try:
                logging.info(f"Attempting to send email to {to_email}...")

                with smtplib.SMTP(email_host, email_port) as server:
                    server.set_debuglevel(1)  # Enable debug mode
                    server.starttls()
                    logging.info("Starting TLS encryption...")

                    # Attempt to log in
                    server.login(email_user, email_password)
                    logging.info("Logged in successfully...")

                    # Send the email
                    server.sendmail(email_user, msg['To'].split(", "), msg.as_string())
                    logging.info(f"Application email sent successfully to {to_email}")
                    break  # Exit the retry loop on successful email
            except Exception as e:
                logging.error(f"Error sending email to {to_email}: {str(e)}", exc_info=True)
                if attempt < retries - 1:
                    logging.info(f"Retrying... (Attempt {attempt + 2} of {retries})")
                    time.sleep(5)  # Wait 5 seconds before retrying
                else:
                    logging.error("All retry attempts failed.")

    except Exception as e:
        logging.error(f"An error occurred while preparing to send the email: {str(e)}", exc_info=True)

# Example usage for sending an application email
logging.info("Sending email...")
send_job_application_email(
    to_email="recipient@example.com",
    job_title="Data Scientist",
    company="TechCorp",
    applicant_name="John Doe",  # Name of the applicant
    cv_path="path_to_uploaded_cv.pdf"  # Path to uploaded CV
)
logging.info("Email function executed.")
