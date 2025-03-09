from flask import Flask, render_template, request, redirect, url_for
import os
from firebase_storage import upload_to_firebase
from cv_parser import extract_cv_data, store_in_google_sheets
from webhook_sender import send_webhook
from email_sender import send_follow_up_email
import threading
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            cv = request.files['cv']

            # Validate file
            if not cv or cv.filename == '':
                return "No CV file selected", 400

            if not (cv.filename.endswith('.pdf') or cv.filename.endswith('.docx')):
                return "Only PDF or DOCX files are supported", 400

            # Save the CV file locally
            cv_filename = os.path.join(app.config['UPLOAD_FOLDER'], cv.filename)
            cv.save(cv_filename)
            logger.info(f"CV saved locally: {cv_filename}")

            # Upload to Firebase
            cv_link = upload_to_firebase(cv_filename, f"cv_folder/{cv.filename}")
            logger.info(f"CV uploaded to Firebase: {cv_link}")

            # Parse CV
            parsed_data = extract_cv_data(cv_filename)
            parsed_data['personal_info'] = {
                "name": name,
                "email": email,
                "phone": phone
            }
            logger.info(f"CV parsed successfully: {parsed_data}")

            # Store in Google Sheets
            store_in_google_sheets(parsed_data, cv_link)
            logger.info("Data stored in Google Sheets")

            # Send webhook
            send_webhook("sewvandichandima@gmail.com", parsed_data, cv_link, name, email, status="prod")
            logger.info("Webhook sent successfully")

            # Send follow-up email in background
            threading.Thread(target=send_follow_up_email, args=(email, name)).start()
            logger.info("Follow-up email scheduled")

            # Clean up local file
            os.remove(cv_filename)
            logger.info(f"Local file removed: {cv_filename}")

            # Redirect to success page
            return redirect(url_for('index', success=True))

        except Exception as e:
            logger.error(f"Error processing application: {str(e)}")
            return f"An error occurred: {str(e)}", 500

    # Render the form
    return render_template('index.html', success=request.args.get('success', False))

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)