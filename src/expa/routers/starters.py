from fastapi import APIRouter, FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import random

from expa.models.starter import Starter, UpdateStarterRequestBody
from expa.persistence.starter_persist import (
    add_starter,
    update_starter as update_starter_db,
    remove_starter,
    get_starters,
    get_starters_by_topic_names
)

router = APIRouter(prefix="/api/v1", tags=["converse"])

@router.get("/starters")
def fetch_starter(topics: Optional[List[str]] = Query(None), isRandom: bool = False):
    try:
        if topics:
            starters = get_starters_by_topic_names(topics)
        else:
            starters = get_starters()

        if isRandom and starters:
            return [random.choice(starters)]

        return starters
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/manage/starters")
def update_starter(request: UpdateStarterRequestBody):
    now = datetime.utcnow()

    try:
        if request.operation_type == 'I':
            if not request.topic_name:
                raise HTTPException(status_code=400, detail="Topic name is required for creation")
            starter_id = str(uuid.uuid4())
            new_starter = Starter(
                starter_id=starter_id,
                topic_name=request.topic_name,
                starter_message=request.starter_message,
                updated_by=request.updated_by,
                updated_ts=now
            )
            add_starter(new_starter)
            return {"message": "Starter created", "starter_id": starter_id}

        elif request.operation_type == 'U':
            if not request.starter_id:
                raise HTTPException(status_code=400, detail="Starter ID required for update")
            updated_starter = Starter(
                starter_id=request.starter_id,
                topic_name=request.topic_name or "",  # fallback to empty string if not provided
                starter_message=request.starter_message,
                updated_by=request.updated_by,
                updated_ts=now
            )
            update_starter_db(updated_starter)
            return {"message": "Starter updated"}

        elif request.operation_type == 'D':
            if not request.starter_id:
                raise HTTPException(status_code=400, detail="Starter ID required for deletion")
            remove_starter(request.starter_id)
            return {"message": "Starter deleted"}

        else:
            raise HTTPException(status_code=400, detail="Invalid operation type")

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
