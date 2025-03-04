import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

logging.basicConfig(level=logging.INFO)

def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = "your_email@example.com"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("your_email@example.com", "your_password")
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            logging.info(f"Email sent successfully to {to_email}")
    except Exception as e:
        logging.error(f"Error sending email to {to_email}: {e}")
