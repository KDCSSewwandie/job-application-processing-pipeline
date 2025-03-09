import requests
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def send_webhook(candidate_email, cv_data, cv_link, name, email, status="prod"):
    """
    Send an HTTP POST request to the webhook endpoint with the processed CV data.

    Args:
        candidate_email (str): The email you used to apply to Metana.
        cv_data (dict): Extracted CV data with keys: personal_info, education, qualifications, projects.
        cv_link (str): Public URL of the uploaded CV.
        name (str): Applicant's name.
        email (str): Applicant's email.
        status (str): "testing" during development, "prod" for final submission.
    """
    try:
        # Webhook endpoint URL
        url = "https://rnd-assignment.automations-3d6.workers.dev/"

        # Headers including the custom X-Candidate-Email header
        headers = {
            "X-Candidate-Email": candidate_email,  # Your email used to apply to Metana
            "Content-Type": "application/json"
        }

        # Payload with CV data and metadata
        payload = {
            "cv_data": {
                "personal_info": cv_data.get("personal_info", {}),
                "education": cv_data.get("education", []),
                "qualifications": cv_data.get("qualifications", []),
                "projects": cv_data.get("projects", []),
                "cv_public_link": cv_link
            },
            "metadata": {
                "applicant_name": name,
                "email": email,
                "status": status,  # "testing" or "prod"
                "cv_processed": True,  # Indicates that the CV was processed
                "processed_timestamp": datetime.utcnow().isoformat() + "Z"  # Timestamp in ISO format
            }
        }

        # Log the payload for debugging
        logger.debug(f"Sending webhook payload: {json.dumps(payload, indent=2)}")

        # Send the POST request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)

        # Log success
        logger.info(f"Webhook sent successfully: {response.status_code} - {response.text}")
        return response

    except requests.exceptions.HTTPError as http_err:
        # Log HTTP errors (e.g., 4xx, 5xx)
        logger.error(f"HTTP error occurred while sending webhook: {http_err} - {response.text}")
    except requests.exceptions.RequestException as req_err:
        # Log request errors (e.g., connection errors)
        logger.error(f"Request error occurred while sending webhook: {req_err}")
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error while sending webhook: {str(e)}")


# Example usage (for testing)
if __name__ == "__main__":
    # Sample data
    candidate_email = "your-email@used-to-apply-to-metana.com"  # Replace with your email
    cv_data = {
        "personal_info": {"name": "John Doe", "email": "john.doe@example.com", "phone": "123-456-7890"},
        "education": ["BS in Computer Science, XYZ University"],
        "qualifications": ["Python", "JavaScript"],
        "projects": ["Project A", "Project B"]
    }
    cv_link = "https://example.com/cv.pdf"
    name = "John Doe"
    email = "john.doe@example.com"
    status = "testing"  # Use "prod" for final submission

    # Send the webhook
    send_webhook(candidate_email, cv_data, cv_link, name, email, status)