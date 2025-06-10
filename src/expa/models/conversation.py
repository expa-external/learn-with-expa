from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ConversationRequestBody(BaseModel):
    user_input: str | None = None
    continue_conversation: bool | None = None
    end_conversation: bool | None = None
    user_first_name: str | None = None
    conversation_id: str | None = None


class ConversationResponseBody(BaseModel):
    conversation_id: str
    model_response: str


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    MODEL = "model"


class Chat(BaseModel):
    text: str
    role: Role
    timestamp: datetime | None = None
    embedding: List[float] | None = None


class Conversation(BaseModel):
    conversation_id: str
    conversation_state: str
    user_id: str
    chat_history: List[Chat]
    creation_ts: datetime
    updated_ts: datetime
    summary: Optional[str] = None
