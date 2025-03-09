import os
import re
import logging
from pdfminer.high_level import extract_text
from docx import Document
import gspread
from google.oauth2.service_account import Credentials

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Google Sheets API credentials
SERVICE_ACCOUNT_FILE = "E:\job-application-pipeline\job-application-c9ba7-firebase-adminsdk-fbsvc-d5f0aa1378.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

try:
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    
    # Open your specific spreadsheet by URL
    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1oNsR7IfrigO-WwQwjdwTvDycvDM8aunPAZD6xns1qzs/edit#gid=0")
    sheet = spreadsheet.sheet1  # Use the first sheet
    logger.info(" Connected to Google Sheets successfully")
except Exception as e:
    logger.error(f" Google Sheets authentication failed: {str(e)}")
    raise

def extract_cv_data(cv_path):
    try:
        if cv_path.endswith('.pdf'):
            text = extract_text(cv_path)
        elif cv_path.endswith('.docx'):
            doc = Document(cv_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            raise ValueError("Unsupported file format")

        if not text.strip():
            logger.warning("⚠ No text extracted from CV")
            return {"personal_info": {}, "education": [], "qualifications": [], "projects": []}

        # Extract personal info
        personal_info = {
            "name": extract_name(text) or "Unknown",
            "email": extract_email(text) or "Unknown",
            "phone": extract_phone(text) or "Unknown"
        }

        # Extract education
        education = extract_education(text)

        # Extract qualifications
        qualifications = extract_qualifications(text)

        # Extract projects
        projects = extract_projects(text)

        return {
            "personal_info": personal_info,
            "education": education,
            "qualifications": qualifications,
            "projects": projects
        }
    except Exception as e:
        logger.error(f"❌ Error parsing CV: {str(e)}")
        return {"personal_info": {}, "education": [], "qualifications": [], "projects": []}

def extract_name(text):
    # Match names like "John Doe" or "John D. Doe"
    match = re.search(r"\b([A-Z][a-z]+(?: [A-Z][a-z]+)*\b", text)
    return match.group(0) if match else None

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    return match.group(0) if match else None

def extract_education(text):
    # Match education sections like "Bachelor of Science in Computer Science"
    education = re.findall(r"(Bachelor|Master|Ph\.?D|B\.Sc|M\.Sc)\.?.*?(?=\n\n|\n[A-Z]|$)", text, re.DOTALL)
    logger.info(f"Extracted Education: {education}")
    return education or []

def extract_qualifications(text):
    # Match qualifications like "Certified Python Developer"
    qualifications = re.findall(r"(Certified|Certification|Diploma|License).*?(?=\n\n|\n[A-Z]|$)", text, re.DOTALL)
    logger.info(f"Extracted Qualifications: {qualifications}")
    return qualifications or []

def extract_projects(text):
    # Match project sections like "Project: Online Shopping System"
    projects = re.findall(r"(Project|Experience|Work):?\s*(.*?)(?=\n\n|\n[A-Z]|$)", text, re.DOTALL)
    logger.info(f"Extracted Projects: {projects}")
    return projects or []

def store_in_google_sheets(data, cv_link):
    try:
        row = [
            data["personal_info"].get("name", "Unknown"),
            data["personal_info"].get("email", "Unknown"),
            data["personal_info"].get("phone", "Unknown"),
            "; ".join(data["education"]),
            "; ".join(data["qualifications"]),
            "; ".join([p[1] for p in data["projects"]]),
            cv_link
        ]
        logger.info(f"Storing row in Google Sheets: {row}")
        sheet.append_row(row)
        logger.info(" Data stored in Google Sheets successfully")
    except Exception as e:
        logger.error(f" Error storing in Google Sheets: {str(e)}")