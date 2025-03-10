import firebase_admin
from firebase_admin import credentials, firestore
import os

# Check if Firebase is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("E:\job-application-pipeline\job-application-c9ba7-804aca363d69.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def store_in_firestore(parsed_data, cv_link):
    doc_ref = db.collection('applications').document(parsed_data['personal_info'].get('name', 'Unknown'))
    doc_ref.set({
        "personal_info": parsed_data["personal_info"],
        "education": parsed_data["education"],
        "qualifications": parsed_data["qualifications"],
        "projects": parsed_data["projects"],
        "cv_public_link": cv_link
    })
