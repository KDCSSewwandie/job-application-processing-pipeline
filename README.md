
# Job Application Processing Pipeline

This project is a submission for the **Software Engineering Intern (RnD) Assignment** at **Metana**. It automates the process of handling job applications, including CV uploads, data extraction, storage, and follow-up email notifications. Below is an overview of the project components and features.

## Features Included

1. **Job Application Form**  
   - A web form built using **Flask** (Python) to collect applicant information, including:
     - Name
     - Email
     - Phone Number
     - CV Upload (PDF or DOCX format)

2. **Cloud Storage for CVs**  
   - Uploaded CVs are stored in **Firebase Storage**, and a publicly accessible link is generated for each CV.

3. **CV Parsing**  
   - The CVs are parsed using Python libraries (`pdfminer.six` for PDFs and `python-docx` for DOCX files) to extract the following information:
     - Personal Info (Name, Contact Details)
     - Education
     - Qualifications
     - Projects

4. **Data Storage**  
   - Extracted data is stored in a **Google Sheet** along with the public link to the CV.

5. **Webhook Integration**  
   - After processing each CV, an HTTP request is sent to the provided endpoint (`https://md-assignment.automations-3d6.workers.dev/`) with the following details:
     - Custom header: `X-Candidate-Email` (to identify submissions)
     - Payload: Processed CV data and metadata (applicant name, email, status, timestamp, etc.)

6. **Follow-Up Email**  
   - A follow-up email is sent to the applicant using **SendGrid** to inform them that their CV is under review.

7. **Cost Optimization and Scalability**  
   - The project is designed to be cost-efficient for small-scale use (100 applications/month) and scalable for larger volumes (1M applications/month).  
   - Detailed cost breakdowns and scalability considerations are provided in the documentation.

## Missing Component: Live Hosted Form  
Unfortunately, the live hosted form is not included due to technical issues encountered while trying to deploy the application on **PythonAnywhere**. Despite multiple attempts, errors related to dependencies and configuration prevented successful deployment. 


## Tech Stack

- **Web Framework**: Flask (Python)  
- **Cloud Storage**: Firebase Storage  
- **Data Storage**: Google Sheets  
- **Email Service**: SendGrid  
- **CV Parsing Libraries**: `pdfminer.six`, `python-docx`  
- **HTTP Requests**: `requests` library  
- **Environment Management**: `python-dotenv` for secure API key handling  


## Project Structure

job-application-processing-pipeline/
│
├── app.py                  # Flask application for the web form
├── cv_parser.py            # CV parsing logic
├── firebase_utils.py       # Firebase Storage integration
├── google_sheets.py        # Google Sheets integration
├── sendgrid_email.py       # SendGrid email integration
├── webhook.py              # Webhook integration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys, etc.)
├── README.md               # Project overview
└── Documentation.pdf       # Detailed documentation and cost breakdown


## How to Run the Project

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/KDCSSewwandie/job-application-processing-pipeline.git
   ```

2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**  
   - Create a `.env` file and add the following variables:
     ```
     FIREBASE_CREDENTIALS=your_firebase_credentials.json
     GOOGLE_SHEETS_CREDENTIALS=your_google_sheets_credentials.json
     SENDGRID_API_KEY=your_sendgrid_api_key
     ```

4. **Run the Flask Application**  
   ```bash
   python app.py
   ```

5. **Access the Web Form**  
   - Open your browser and navigate to `http://localhost:5000` to access the job application form.

---

## Future Improvements

- **Enhanced CV Parsing**: Improve the parsing logic to handle complex CV formats.  
- **Email Scheduling**: Implement email scheduling based on the applicant's time zone.  
- **Database Upgrade**: Migrate from Google Sheets to a more scalable database like Firestore or PostgreSQL.  
- **Error Handling**: Add robust error handling and logging for better reliability.  
- **Live Deployment**: Resolve deployment issues to host the form live.  

---
