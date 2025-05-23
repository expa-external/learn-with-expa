from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ConversationRequestBody(BaseModel):
    user_input: str
    continue_conversation: bool
    end_conversation: bool

class ConversationResponseBody(BaseModel):
    conversation_id: float
    model_response: str


class Chat(BaseModel):
    text: str
    role: str
    timestamp: datetime

class Conversation(BaseModel):
    conversation_id: str
    conversation_state: str
    user_id: str
    chatHistory: List[Chat]
    creation_ts: datetime
    updated_ts: datetime
    summary: str


