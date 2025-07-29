from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Starter(BaseModel):
    starter_id: str
    topic_name: str
    starter_message: str 
    updated_by: str 
    updated_ts: datetime

class UpdateStarterRequestBody(BaseModel):
    starter_id: Optional[str] = None
    topic_name: Optional[str] = None
    starter_message: str
    updated_by: str
    updated_ts: Optional[datetime] = None
    operation_type: str  # U/I/D