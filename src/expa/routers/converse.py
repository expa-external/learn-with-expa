import datetime

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
# from expa.chat import chat_with_gemini
# from expa.record_audio import record_audio_vad
# from expa.transcribe_audio import transcribe_audio
import uuid

from expa.persistence.conversation_persist import get_conversation_list, add_data_to_collection, get_most_recent_conversation, update_data_to_collection
from expa.models.conversation import ConversationRequestBody, ConversationResponseBody, Conversation, Chat, Role
from expa.service.ConversationService import *

router = APIRouter(prefix="/api/v1", tags=["Converse"])
initial_user_input = ("This is start of the conversation with the user. You are required to initiate the conversation "
                      "understanding how are they and what they want to learn today. The logged in user name is ")


# @router.post("/converse/file", response_model=ConversationResponseBody)
# async def converse(file: UploadFile = File(...)):
#
#     input_audio = await file.read()
#     if not isinstance(input_audio, (bytes, bytearray)):
#         raise HTTPException(status_code=400, detail="Invalid file upload")
#
#     response, elapsed_time = await chat_with_gemini(input_audio)
#
#     return ConversationResponseBody(
#         model_response = response,
#         conversation_id = 100
#     )


@router.post("/converse", response_model=ConversationResponseBody)
async def converse(conversation_request_body: ConversationRequestBody):
    continue_flag = conversation_request_body.continue_conversation
    end_flag = conversation_request_body.end_conversation

    if continue_flag and end_flag:
        raise HTTPException(status_code=400, detail="Cannot continue and end conversation at the same time")
    
    if continue_flag:
        return continue_conversation(conversation_request_body)
    elif end_flag:
        return end_conversation(conversation_request_body)
    else:
        return initiate_conversation(conversation_request_body)
    
    
@router.get("/conversation", response_model=List[Conversation])
async def converse(user_id: str, last_conversations: Optional[int] = None):
    conversationList = get_conversation_list(user_id)
    return conversationList


