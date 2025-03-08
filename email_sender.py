import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

def send_job_application_email(to_email, job_title, company):
    # Get email credentials from environment variables
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_host = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    email_port = int(os.getenv('EMAIL_PORT', 587))

    # Ensure that environment variables are set
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
    [Your Name]
    """

    # Create message object
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = ", ".join(to_email) if isinstance(to_email, list) else to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Start email server and send message
        with smtplib.SMTP(email_host, email_port) as server:
            server.set_debuglevel(1)  # Enable debug mode to view detailed communication
            server.starttls()  # Secure the connection
            server.login(email_user, email_password)
            server.sendmail(email_user, msg['To'].split(", "), msg.as_string())
            logging.info(f"Application email sent successfully to {to_email}")
    except Exception as e:
        logging.error(f"Error sending email to {to_email}", exc_info=True)

# Example usage:
send_job_application_email("recipient@example.com", "Data Scientist", "Tech Corp")