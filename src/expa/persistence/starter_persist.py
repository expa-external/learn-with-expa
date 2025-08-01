import firebase_admin
from datetime import datetime
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1 import ArrayUnion
from google.cloud.firestore_v1.base_query import FieldFilter
import uuid
import logging

from expa_configs import APP_CONFIG, get_active_profile
from expa.models.starter import Starter
from . import firestore_client

logger = logging.getLogger(__name__)

def add_starter(starter: Starter):
    try:
        logger.info(f"Adding starter for topic '{starter.topic_name}'")
        starter_id = uuid.uuid4().hex
        starter_dict = starter.model_dump(exclude_unset=True)
        starter_dict["starter_id"] = starter_id
        starter_dict["updated_ts"] = datetime.now().isoformat()

        doc_ref = firestore_client.connection.collection(firestore_client.starters_collection).document(starter_id)
        doc_ref.set(starter_dict)
        return starter_id
    except Exception as e:
        logger.error(f"Error while adding starter for topic '{starter.topic_name}'", exc_info=True)
        raise e

def remove_starter(starter_id: str):
    try:
        logger.info(f"Removing starter with starter_id={starter_id}")
        docs = (
            firestore_client.connection
            .collection(firestore_client.starters_collection)
            .where("starter_id", "==", starter_id)
            .limit(1)
            .stream()
        )
        doc = next(docs, None)
        if doc:
            doc.reference.delete()
            logger.info(f"Starter with starter_id '{starter_id}' deleted.")
            return starter_id
        else:
            raise ValueError(f"Starter with starter_id '{starter_id}' not found.")
    except Exception as e:
        logger.error(f"Error while removing starter with starter_id '{starter_id}'", exc_info=True)
        raise e

def update_starter(starter: Starter):
    try:
        if not starter.starter_id:
            raise ValueError("Missing 'starter_id' for starter update")

        logger.info(f"Updating starter for topic '{starter.topic_name}' (starter_id={starter.starter_id})")
        docs = (
            firestore_client.connection
            .collection(firestore_client.starters_collection)
            .where("starter_id", "==", starter.starter_id)
            .limit(1)
            .stream()
        )
        doc = next(docs, None)
        if doc:
            existing_data = doc.to_dict()
            update_data = starter.model_dump(exclude_unset=True)

            # Retain existing topic_name if the incoming one is empty
            if "topic_name" in update_data and not update_data["topic_name"]:
                update_data["topic_name"] = existing_data.get("topic_name")

            update_data["updated_ts"] = datetime.now().isoformat()
            doc.reference.update(update_data)
            return starter.starter_id
        else:
            raise ValueError(f"Starter with starter_id '{starter.starter_id}' not found")
    except Exception as e:
        logger.error(f"Error while updating starter for topic '{starter.topic_name}'", exc_info=True)
        raise e

def get_starters() -> list[dict]:
    try:
        logger.info(f"Fetching all starters")
        docs = (
            firestore_client.connection
            .collection(firestore_client.starters_collection)
            .stream()
        )
        starters = []
        for doc in docs:
            data = doc.to_dict()
            if "starter_id" not in data:
                logger.warning(f"Document {doc.id} missing starter_id field")
            starters.append(data)
        logger.info(f"Fetched {len(starters)} starters")
        return starters
    except Exception as e:
        logger.error("Error while fetching all starters", exc_info=True)
        raise e

def get_starter_by_id(starter_id: str) -> dict:
    try:
        logger.info(f"Fetching starter by starter_id: {starter_id}")
        docs = (
            firestore_client.connection
            .collection(firestore_client.starters_collection)
            .where("starter_id", "==", starter_id)
            .limit(1)
            .stream()
        )
        doc = next(docs, None)
        if doc:
            return doc.to_dict()
        else:
            raise ValueError(f"Starter with starter_id '{starter_id}' not found")
    except Exception as e:
        logger.error(f"Error while fetching starter by starter_id '{starter_id}'", exc_info=True)
        raise e

def get_starter_by_topic(topic_name: str) -> dict:
    try:
        logger.info(f"Fetching starter by topic_name: {topic_name}")
        docs = (
            firestore_client.connection
            .collection(firestore_client.starters_collection)
            .where("topic_name", "==", topic_name)
            .limit(1)
            .stream()
        )
        doc = next(docs, None)
        if doc:
            return doc.to_dict()
        else:
            raise ValueError(f"No starter found for topic '{topic_name}'")
    except Exception as e:
        logger.error(f"Error while fetching starter by topic_name '{topic_name}'", exc_info=True)
        raise e

def get_starters_by_topic_names(topic_names: list[str]) -> list[dict]:
    try:
        logger.info(f"Fetching starters by topic_names: {topic_names}")
        
        if not topic_names:
            raise ValueError("Topic names list is empty")

        # Firestore 'in' filter supports up to 10 values
        if len(topic_names) > 10:
            raise ValueError("Firestore 'in' query supports a maximum of 10 topic names")

        docs = (
            firestore_client.connection
            .collection(firestore_client.starters_collection)
            .where("topic_name", "in", topic_names)
            .stream()
        )

        starters = [doc.to_dict() for doc in docs]
        logger.info(f"Fetched {len(starters)} starters")
        return starters

    except Exception as e:
        logger.error(f"Error while fetching starters by topic_names '{topic_names}'", exc_info=True)
        raise e
