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
    user_id: str | None = None
    topic_id: str | None = None


class ConversationResponseBody(BaseModel):
    conversation_id: str | None = None
    model_response: str | None = None


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    MODEL = "model"


class Chat(BaseModel):
    text: str
    role: Role
    timestamp: datetime | None = None
    conversationId: str


class Conversation(BaseModel):
    conversation_id: str
    conversation_state: str
    user_id: str
    chat_history: List[Chat] = None
    creation_ts: datetime
    updated_ts: datetime


class UpdateGuardrails(BaseModel):
    version_id: str
    created_by: str
    created_on: datetime
    user_input: str | None


class GuardrailRequest(BaseModel):
    user_input: str
    user_id: str
