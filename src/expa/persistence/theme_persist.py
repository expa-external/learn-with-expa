
import firebase_admin
from datetime import datetime
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1 import ArrayUnion
from google.cloud.firestore_v1.base_query import FieldFilter
import uuid
import logging

from expa_configs import APP_CONFIG, get_active_profile
from expa.models.theme import Theme
from . import firestore_client

logger = logging.getLogger(__name__)

def add_theme(theme: Theme):
    try:
        logger.info(f"Adding theme '{theme.name}'")
        topic_id = uuid.uuid4().hex
        theme_dict = theme.model_dump(exclude_unset=True)
        theme_dict["topic_id"] = topic_id
        theme_dict["updated_ts"] = datetime.now().isoformat()

        doc_ref = firestore_client.connection.collection(firestore_client.themes_collection).document(topic_id)
        doc_ref.set(theme_dict)
    except Exception as e:
        logger.error(f"Error while adding theme '{theme.name}'", exc_info=True)
        raise e


def remove_theme(topic_id: str):
    try:
        logger.info(f"Removing theme with topic_id={topic_id}")
        docs = (
            firestore_client.connection
            .collection(firestore_client.themes_collection)
            .where("topic_id", "==", topic_id)
            .limit(1)
            .stream()
        )
        doc = next(docs, None)
        if doc:
            doc.reference.delete()
            logger.info(f"Theme with topic_id '{topic_id}' deleted.")
        else:
            raise ValueError(f"Theme with topic_id '{topic_id}' not found.")
    except Exception as e:
        logger.error(f"Error while removing theme with topic_id '{topic_id}'", exc_info=True)
        raise e


def update_theme(theme: Theme):
    try:
        if not theme.topic_id:
            raise ValueError("Missing 'topic_id' for theme update")

        logger.info(f"Updating theme '{theme.name}' (topic_id={theme.topic_id})")
        docs = (
            firestore_client.connection
            .collection(firestore_client.themes_collection)
            .where("topic_id", "==", theme.topic_id)
            .limit(1)
            .stream()
        )
        doc = next(docs, None)
        if doc:
            update_data = theme.model_dump(exclude_unset=True)
            update_data["updated_ts"] = datetime.now().isoformat()
            doc.reference.update(update_data)
        else:
            raise ValueError(f"Theme with topic_id '{theme.topic_id}' not found")
    except Exception as e:
        logger.error(f"Error while updating theme '{theme.name}'", exc_info=True)
        raise e


def get_themes() -> list[dict]:
    try:
        logger.info(f"Fetching all themes")
        docs = (
            firestore_client.connection
            .collection(firestore_client.themes_collection)
            .stream()
        )
        themes = []
        for doc in docs:
            data = doc.to_dict()
            if "topic_id" not in data:
                logger.warning(f"Document {doc.id} missing topic_id field")
            themes.append(data)
        logger.info(f"Fetched {len(themes)} themes")
        return themes
    except Exception as e:
        logger.error("Error while fetching all themes", exc_info=True)
        raise e


def get_theme_by_topic_id(topic_id: str) -> dict:
    try:
        logger.info(f"Fetching theme by topic_id: {topic_id}")
        docs = (
            firestore_client.connection
            .collection(firestore_client.themes_collection)
            .where("topic_id", "==", topic_id)
            .limit(1)
            .stream()
        )
        doc = next(docs, None)
        if doc:
            return doc.to_dict()
        else:
            raise ValueError(f"Theme with topic_id '{topic_id}' not found")
    except Exception as e:
        logger.error(f"Error while fetching theme by topic_id '{topic_id}'", exc_info=True)
        raise e


def get_theme_by_name(name: str) -> dict:
    try:
        logger.info(f"Fetching theme by name: {name}")
        docs = (
            firestore_client.connection
            .collection(firestore_client.themes_collection)
            .where("name", "==", name)
            .limit(1)
            .stream()
        )
        doc = next(docs, None)
        if doc:
            return doc.to_dict()
        else:
            raise ValueError(f"No theme named '{name}' found")
    except Exception as e:
        logger.error(f"Error while fetching theme by name '{name}'", exc_info=True)
        raise e