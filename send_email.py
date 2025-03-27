# Import required libraries
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

# Load environment variables from the .env file
load_dotenv(".env.variables")  

# SMTP Configuration for sending emails
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")

# File to track sent emails and avoid duplicates
SENT_EMAILS_FILE = "sent_emails.txt"


def has_email_been_sent(email):
    """
    Checks if an email has already been sent to avoid duplicate emails.

    Args:
        email (str): The recipient's email address.

    Returns:
        bool: True if the email has already been sent, False otherwise.
    """
    if not os.path.exists(SENT_EMAILS_FILE):
        return False 
    
    with open(SENT_EMAILS_FILE, "r") as file:
        return email in file.read()


def mark_email_as_sent(email):
    """
    Marks an email as sent by writing it to the tracking file.

    Args:
        email (str): The recipient's email address.
    """
    with open(SENT_EMAILS_FILE, "a") as file:
        file.write(email + "\n")


def send_email(recipient_email, name):
    """
    Sends an email to a candidate, ensuring it is not sent multiple times.

    Args:
        recipient_email (str): The email address of the candidate.
        name (str): The candidate's name.
    
    Returns:
        None
    """
    # Ensure email credentials are available
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("❌ Error: Missing email credentials. Skipping email for", name)
        return

    # Prevent duplicate email sending
    if has_email_been_sent(recipient_email):
        print(f"⚠️ Email already sent to {recipient_email}, skipping...")
        return

    # Email subject and body
    subject = "Application Update"
    body = f"Hi {name}, thanks for applying! Based on our initial screening, we'd like to move forward with your application."

    # Create email message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email

    try:
        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection with TLS
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Authenticate sender
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())  # Send email

        mark_email_as_sent(recipient_email)  # Track sent email
        print(f"✅ Email sent to {recipient_email}")

    except smtplib.SMTPAuthenticationError:
        print(f"❌ Authentication Error: Check your credentials.")
    except smtplib.SMTPException as e:
        print(f"❌ Email Error: {e}")
