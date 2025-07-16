from fastapi import APIRouter, File, HTTPException

from expa.persistence.conversation_persist import get_conversation_list, add_data_to_collection, get_most_recent_conversation, update_data_to_collection
from expa.persistence.theme_persist import get_themes, get_theme_by_topic_id, update_theme, remove_theme, add_theme
from expa.models.theme import Theme
from expa.service.ConversationService import *

router = APIRouter(prefix="/api/v1/theme", tags=["converse"])

@router.post("/add", status_code=201)
async def add_theme_endpoint(theme: Theme):
    try:
        add_theme(theme)
        return {"message": "Theme added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add theme: {str(e)}")

@router.delete("/remove/{topic_id}", status_code=200)
async def remove_theme_endpoint(topic_id: str):
    try:
        remove_theme(topic_id)
        return {"message": "Theme removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove theme: {str(e)}")

@router.put("/update", status_code=200)
async def update_theme_endpoint(theme: Theme):
    try:
        update_theme(theme)
        return {"message": "Theme updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update theme: {str(e)}")

@router.get("/", status_code=200)
async def get_theme():
    try:
        themes = get_themes()
        return {"themes": themes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch themes: {str(e)}")

@router.get("/{topic_id}", status_code=200)
async def get_theme_by_id(topic_id: str):
    try:
        theme = get_theme_by_topic_id(topic_id)
        return {"theme": theme}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch theme: {str(e)}")
        