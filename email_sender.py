import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from datetime import datetime, timedelta
import pytz
from threading import Timer

logger = logging.getLogger(__name__)

def send_follow_up_email(email, name, timezone="UTC"):
    """
    Send a follow-up email to the applicant the next day at a convenient time.

    Args:
        email (str): Applicant's email address.
        name (str): Applicant's name.
        timezone (str): Applicant's time zone (e.g., "America/New_York").
    """
    try:
        # Email configuration
        sender_email = "noreply@metana.io"  # Replace with your email
        sender_password = "your-email-password"  # Replace with your email password
        subject = "Your CV is Under Review"
        body = f"Dear {name},\n\nYour CV has been received and is under review. Thank you for applying!\n\nBest regards,\nMetana Team"

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Calculate the send time (next day at 10:00 AM in the applicant's timezone)
        applicant_timezone = pytz.timezone(timezone)
        now = datetime.now(applicant_timezone)
        send_time = (now + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)

        # If the send time is in the past (e.g., if it's already after 10:00 AM), schedule for the next day
        if send_time < now:
            send_time += timedelta(days=1)

        # Convert send time to UTC for scheduling
        utc_timezone = pytz.utc
        send_time_utc = send_time.astimezone(utc_timezone)
        delay = (send_time_utc - datetime.now(utc_timezone)).total_seconds()

        # Schedule the email
        Timer(delay, _send_email, args=(sender_email, sender_password, msg)).start()
        logger.info(f"Follow-up email scheduled for {send_time} ({timezone})")

    except Exception as e:
        logger.error(f"Error scheduling follow-up email: {str(e)}")
        raise

def _send_email(sender_email, sender_password, msg):
    """
    Helper function to send the email.
    """
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        logger.info(f"Follow-up email sent to {msg['To']}")
    except Exception as e:
        logger.error(f"Error sending follow-up email: {str(e)}")
        raise