import datetime
import logging
import firebase_admin
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1 import ArrayUnion

from ..expa_configs import APP_CONFIG, get_active_profile
from ..expa.models.conversation import Conversation, Chat

logger = logging.getLogger(__name__)


def update_summary_after_completion(session_id: str, summary: str):
    try:
        logger.info(f"Updating the summary for conversation with session id: {session_id}")
        doc_ref = ConversationPersist.connection.collection(ConversationPersist.collection).document(session_id)
        if doc_ref.exists:
            doc_ref.update({'summary': summary})
            doc_ref.update({'updated_ts': datetime.datetime.now().isoformat()})
            logger.info(f"Successfully updated the conversation with conversation id: {session_id}")
        else:
            logger.error(f"No conversation found with conversation id: {session_id}")
            raise ValueError(f"No conversation found with conversation id: {session_id}")
    except Exception as e:
        logger.error(f"Error while updating the conversation with conversation id: {session_id}")
        raise e


def add_data_to_collection(conversation: Conversation):
    try:
        logger.info(f"Creating a new document for session id: {conversation.conversation_id}")
        doc_ref = (ConversationPersist.connection.collection(ConversationPersist.collection)
                   .document(conversation.conversation_id))
        doc_ref.set(conversation.model_dump())
    except Exception as e:
        logger.error(f"Error while creating a new document for session id {conversation.conversation_id}", e)
        raise e


def update_data_to_collection(chat: Chat, session_id: str):
    try:
        logger.info(f"Adding a new chat to document with session id: {session_id}")
        doc_ref = ConversationPersist.connection.collection(ConversationPersist.collection).document(session_id)
        if doc_ref.exists:
            doc_ref.update({'chatHistory': ArrayUnion([chat])})
            doc_ref.update({'updated_ts': datetime.datetime.now().isoformat()})
        else:
            logger.error(f"No conversation found with conversation id: {session_id}")
            raise ValueError(f"No conversation found with conversation id: {session_id}")
    except Exception as e:
        logger.error(f"Error while updating the conversation with conversation id: {session_id}")
        raise e


def get_conversation_list() -> list[Conversation]:
    
    try:
        logger.info("Fetching conversation list from Firestore")
        docs = (ConversationPersist.connection
                .collection(ConversationPersist.collection)
                .stream())

        conversation_list = []
        for doc in docs:
            data = doc.to_dict()
            # Convert Firestore dict to Conversation model
            conversation = Conversation(**data)
            conversation_list.append(conversation)

        logger.info(f"Fetched {len(conversation_list)} conversations")
        return conversation_list

    except Exception as e:
        logger.error("Error fetching conversation list from Firestore", exc_info=True)
        raise e

class ConversationPersist(object):
    connection = None
    collection = 'conversations'

    def __init__(self):
        if ConversationPersist.connection is None:
            if get_active_profile() == "local":
                cred = credentials.Certificate(APP_CONFIG['google']['firestore']['service-account-file'])
                firebase_admin.initialize_app(credential=cred)
            else:
                firebase_admin.initialize_app()
            ConversationPersist.connection = firestore.client()

ConversationPersist()
