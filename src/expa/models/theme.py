from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Theme(BaseModel):
    topic_id: str
    name: str
    short_description: Optional[str] = None
    scenarios: Optional[List[str]] = None
    updated_by: Optional[str] = None
    updated_ts: datetime
