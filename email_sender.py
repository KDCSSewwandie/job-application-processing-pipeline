import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import logging
from datetime import datetime, timedelta
import pytz
from threading import Timer

logger = logging.getLogger(__name__)

def send_follow_up_email(email, name, timezone="UTC", sendgrid_api_key="your-sendgrid-api-key"):
    """
    Send a follow-up email to the applicant the next day at a convenient time.

    Args:
        email (str): Applicant's email address.
        name (str): Applicant's name.
        timezone (str): Applicant's time zone (e.g., "America/New_York").
        sendgrid_api_key (str): Your SendGrid API key.
    """
    try:
        # Email configuration
        sender_email = "sewvandichandima@gmail.com"  # Replace with your email
        subject = "Your CV is Under Review"
        body = f"Dear {name},\n\nYour CV has been received and is under review. Thank you for applying!\n\nBest regards,\nMetana Team"

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
        Timer(delay, _send_email, args=(sendgrid_api_key, sender_email, email, subject, body)).start()
        logger.info(f"Follow-up email scheduled for {send_time} ({timezone})")

    except Exception as e:
        logger.error(f"Error scheduling follow-up email: {str(e)}")
        raise

def _send_email(sendgrid_api_key, sender_email, recipient_email, subject, body):
    """
    Helper function to send the email using SendGrid.
    """
    try:
        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
        from_email = Email(sender_email)
        to_email = To(recipient_email)
        content = Content("text/plain", body)
        mail = Mail(from_email, to_email, subject, content)

        # Send email
        response = sg.send(mail)
        if response.status_code == 202:
            logger.info(f"Follow-up email sent to {recipient_email}")
        else:
            logger.error(f"Failed to send email. Status code: {response.status_code}")
            logger.error(f"Response body: {response.body}")

    except Exception as e:
        logger.error(f"Error sending follow-up email: {str(e)}")
        raise
