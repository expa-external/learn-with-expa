import firebase_admin
from datetime import datetime
from firebase_admin import firestore, credentials
from expa_configs import APP_CONFIG, get_active_profile
from firebase_admin import _apps

class FirestoreClient(object):
    connection = None
    conversations_collection = 'conversations'
    guardrails_collection = 'guardrails'
    themes_collection = 'themes'

    def __init__(self):
        if FirestoreClient.connection is None:
            if not firebase_admin._apps:
                if get_active_profile() == "local":
                    cred = credentials.Certificate("cadet-user-firebase-adminsdk-fbsvc-310d513553.json")
                    firebase_admin.initialize_app(credential=cred, options={'projectId': 'cadet-user'})
                else:
                    firebase_admin.initialize_app()
            FirestoreClient.connection = firestore.client()

firestore_client = FirestoreClient()