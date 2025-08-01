import logging

from expa.models.conversation import UpdateGuardrails
from . import firestore_client
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

logger = logging.getLogger(__name__)

def update_guardrails_for_model(user_input: UpdateGuardrails):
    try:
        logger.info(f"Guardrails for model updated by user {user_input.created_by}")
        doc_ref = (firestore_client.connection.collection(firestore_client.guardrails_collection)
                   .document(user_input.version_id))
        doc_ref.set(user_input.model_dump())
    except Exception as e:
        logger.error(f"Error while creating a new version for guardrails", e)
        raise e


def fetch_last_updated_guardrails_for_model() -> str:
    try:
        logger.info("Fetching last updated guardrails entered by user.")
        docs = (firestore_client.connection.collection(firestore_client.guardrails_collection)
                .where(filter=FieldFilter("user_input", "!=", ""))
                .order_by("created_on", direction=firestore.Query.DESCENDING)
                .limit(1)
                .stream()
                )
        latest_doc = next(docs, None)
        if latest_doc is not None:
            return latest_doc.to_dict().get("user_input")
        return ""
    except Exception as e:
        logger.error("Error while fetching last version for guardrails", e)
        raise e