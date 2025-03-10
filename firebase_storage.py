import firebase_admin
from firebase_admin import credentials, storage
import os
import logging

logger = logging.getLogger(__name__)

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("E:\job-application-pipeline\job-application-c9ba7-804aca363d69.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'job-application-c9ba7.firebasestorage.app'
    })

def upload_to_firebase(file_path, destination_path):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(destination_path)
        blob.upload_from_filename(file_path)
        blob.make_public()
        return blob.public_url
    except Exception as e:
        logger.error(f"Error uploading to Firebase: {str(e)}")
        raise
    
    