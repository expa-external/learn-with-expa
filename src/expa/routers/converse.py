from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
from ..chat import chat_with_gemini 
from ..record_audio import record_audio_vad 
from ..transcribe_audio import transcribe_audio

from ..models.conversation import ConversationRequestBody, ConversationResponseBody, Conversation

router = APIRouter(prefix="/converse", tags=["converse"])

@router.post("/api/v1/converse/file", response_model=ConversationResponseBody)
async def converse(file: UploadFile = File(...)):

    input_audio = await file.read()
    if not isinstance(input_audio, (bytes, bytearray)):
        raise HTTPException(status_code=400, detail="Invalid file upload")

    response, elapsed_time = await chat_with_gemini(input_audio)

    return ConversationResponseBody(
        model_response = response,
        conversation_id = "conversationId"
    )

@router.post("/api/v1/converse", response_model=ConversationResponseBody)
async def converse(conversation_request_body: ConversationRequestBody):

    input_text = conversation_request_body.user_input
    
    # response = chat_with_gemini_model()
    response = ""

    return ConversationResponseBody(
        model_response = "",
        conversation_id = "conversationId"
    )

@router.get("/api/v1/conversation", response_model=List[Conversation])
async def converse(user_id: str, last_conversations: Optional[int] = None):
    conversationList = []
    return conversationList