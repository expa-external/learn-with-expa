import datetime
import logging
import uuid

import firebase_admin
from datetime import datetime
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1 import ArrayUnion, FieldFilter
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector

from ..expa_configs import APP_CONFIG, get_active_profile
from ..expa.models.conversation import Conversation, Chat

logger = logging.getLogger(__name__)


def update_summary_after_completion(session_id: str):
    try:
        logger.info(f"Updating the summary for conversation with session id: {session_id}")
        doc_ref = ConversationPersist.connection.collection(ConversationPersist.collection).document(session_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update({'conversation_state': "ENDED"})
            doc_ref.update({'updated_ts': datetime.now().isoformat()})
            logger.info(f"Successfully updated the conversation with conversation id: {session_id}")
        else:
            logger.error(f"No conversation found with conversation id: {session_id}")
            raise ValueError(f"No conversation found with conversation id: {session_id}")
    except Exception as e:
        logger.error(f"Error while updating the conversation with conversation id: {session_id}")
        raise e


def add_data_to_collection(conversation: Conversation, chat: Chat):
    try:
        logger.info(f"Creating a new document for session id: {conversation.conversation_id}")
        doc_ref = (ConversationPersist.connection.collection(ConversationPersist.collection)
                   .document(conversation.conversation_id))
        doc_ref.set(conversation.model_dump())
        logger.info(f"Adding a new chat turn for conversation id {conversation.conversation_id}")
        chat_ref = (ConversationPersist.connection.collection(ConversationPersist.conversationTurn)
                    .document(str(uuid.uuid4())))
        chat_ref.set(chat.model_dump())
    except Exception as e:
        logger.error(f"Error while creating a new document for session id {conversation.conversation_id}", e)
        raise e


def update_data_to_collection(chat: Chat):
    try:
        logger.info(f"Adding a new chat to chat turn collection for conversation id: {chat.conversationId}")
        doc_ref = (ConversationPersist.connection.collection(ConversationPersist.conversationTurn)
                   .document(str(uuid.uuid4())))
        doc_ref.set(chat.model_dump())
    except Exception as e:
        logger.error(f"Error while updating the conversation with conversation id: {chat.conversationId}")
        raise e


def retrieve_context_from_embeddings(chat: Chat, conversation_id: str, k: int):
    try:
        logger.info(f"Fetching {k} similar conversation for the conversation id: {conversation_id} "
                    f"to fetch the context")
        conversation_turn = (ConversationPersist.connection.collection(ConversationPersist.conversationTurn))
        query = conversation_turn.where(filter=FieldFilter("conversationId", "==", conversation_id))
        print(chat.embedding)
        vector_query = query.find_nearest(
            vector_field="embedding",
            query_vector=Vector(chat.embedding),
            distance_measure=DistanceMeasure.COSINE,
            limit=k,
        )
        retrieved_chats_data = []
        # # for doc in query.stream():
        # #     data = doc.to_dict()
        # #     chat = Chat(**data)
        # #     retrieved_chats_data.append(chat)
        # print("Retrieved Chats" + str(retrieved_chats_data))
        for doc_snapshot in vector_query.stream():
            # Each doc_snapshot is a DocumentSnapshot object
            chat_data = doc_snapshot.to_dict()
            if chat_data: # Ensure there's data
                retrieved_chats_data.append(chat_data)
        print("Retrieved Chats" + str(retrieved_chats_data))
        # Optional but highly recommended: Sort by timestamp for chronological context
        # assuming 'timestamp' is a datetime object or a string that can be sorted
        sorted_chats_data = sorted(retrieved_chats_data, key=lambda x: x.get('timestamp', datetime.min))
        logger.info(f"Successfully retrieved {len(sorted_chats_data)} relevant chat turns.")
        return sorted_chats_data
    except Exception as e:
        logger.error(f"Error while fetching similar conversation for conversation id: {conversation_id}")
        raise e



def get_conversation_list(user_id: str) -> list[Conversation]:
    try:
        logger.info("Fetching conversation list from Firestore")
        docs = (ConversationPersist.connection
                .collection(ConversationPersist.collection)
                .where("user_id", "==", user_id)
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

def get_most_recent_conversation(user_id: str) -> Conversation:
    try:
        docs = (
                ConversationPersist.connection
                .collection(ConversationPersist.collection)
                .where("user_id", "==", user_id)
                .order_by("updated_ts", direction=firestore.Query.DESCENDING)
                .limit(1)
                .stream()
            )
        latest_doc = next(docs, None)
        return latest_doc
    except Exception as e:
        logger.error("Error fetching most recent conversation from Firestore", exc_info=True)
        raise e

class ConversationPersist(object):
    connection = None
    collection = 'conversations'
    conversationTurn = 'conversation_turn'

    def __init__(self):
        if ConversationPersist.connection is None:
            if get_active_profile() == "local":
                cred = credentials.Certificate(APP_CONFIG['google']['firestore']['service-account-file'])
                firebase_admin.initialize_app(credential=cred)
            else:
                firebase_admin.initialize_app()
            ConversationPersist.connection = firestore.client()

ConversationPersist()
