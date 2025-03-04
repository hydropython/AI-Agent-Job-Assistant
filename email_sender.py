import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

def send_email(subject, body, to_email):
    # Create message object
    msg = MIMEMultipart()
    msg['From'] = "your_email@example.com"  # Replace with your email address
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Get email credentials from environment variables for security reasons
        email_user = os.getenv('EMAIL_USER', 'your_email@example.com')  # Set your email in the environment variable or hardcode
        email_password = os.getenv('EMAIL_PASSWORD', 'your_password')  # Set your email password in the environment variable or use App Password

        # Start email server and send message
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(email_user, email_password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            logging.info(f"Email sent successfully to {to_email}")
    except Exception as e:
        logging.error(f"Error sending email to {to_email}: {e}")

# Example usage:
send_email('Test Subject', 'This is the email body', 'recipient@example.com')
