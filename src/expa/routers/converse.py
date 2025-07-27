import datetime
import base64

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import Response
from typing import List, Optional
from pydantic import BaseModel
# from expa.chat import chat_with_gemini
# from expa.record_audio import record_audio_vad
# from expa.transcribe_audio import transcribe_audio
import uuid

from expa.persistence.conversation_persist import get_conversation_list, add_data_to_collection, get_most_recent_conversation, update_data_to_collection
from expa.models.conversation import ConversationRequestBody, ConversationResponseBody, Conversation, Chat, Role
from expa.service.ConversationService import *

router = APIRouter(prefix="/api/v1", tags=["converse"])
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

# @router.post("/converse", response_model=ConversationResponseBody)
# async def converse(conversation_request_body: ConversationRequestBody):
#     response = ""
#     conversation_id = ""
#     if conversation_request_body.continue_conversation is False:
#         conversation_id = str(uuid.uuid4())
#         # initiateCache(conversation_id)
#         response = initiateConversation(initial_user_input + conversation_request_body.user_first_name)
#         chat = Chat(
#             text=response,
#             role=Role.SYSTEM,
#             timestamp=datetime.datetime.now()
#         )
#         conversation = Conversation(
#             conversation_id=conversation_id,
#             conversation_state='ACTIVE',
#             user_id=conversation_request_body.user_first_name,
#             creation_ts=datetime.datetime.now(),
#             updated_ts=datetime.datetime.now(),
#             chat_history=[chat]
#         )
#         add_data_to_collection(conversation)
#         return ConversationResponseBody(
#             model_response=response,
#             conversation_id=conversation_id
#         )
#     else:
#         user_id = conversation_request_body.user_first_name
#         # Fetch most recent conversation
#         latest_doc_ref = get_most_recent_conversation(user_id=user_id)
#         conversation = latest_doc_ref.to_dict()
#         conversation_id = conversation["conversation_id"]
#
#         # Add user input to chat history
#         user_chat = Chat(
#             text=conversation_request_body.user_input,
#             role=Role.USER,
#             timestamp=datetime.datetime.now()
#         )
#         update_data_to_collection(user_chat, conversation_id)
#
#         # Get system response
#         response = initiateConversation(user_input=conversation_request_body.user_input)
#
#         system_chat = Chat(
#             text=response,
#             role=Role.SYSTEM,
#             timestamp=datetime.datetime.now()
#         )
#         update_data_to_collection(system_chat, conversation_id)
#         return ConversationResponseBody(
#             model_response=response,
#             conversation_id=conversation_id
#         )



@router.post("/converse", response_model=ConversationResponseBody)
async def converse(conversation_request_body: ConversationRequestBody):
    if conversation_request_body.continue_conversation is False:
        return initiate_conversation(conversation_request_body)
    elif conversation_request_body.continue_conversation is True:
        return continue_conversation(conversation_request_body)
    elif conversation_request_body.end_conversation is True:
        return end_conversation(conversation_request_body)

@router.post("/speech-to-text", status_code=200)
async def convert_audio_input_to_text(audio_file: UploadFile = File(...)):
    try:
        if not audio_file.filename:
            raise HTTPException(status_code=400, detail="No File Uploaded")
        if audio_file.content_type not in ["audio/wav", "audio/amr"]:
            raise HTTPException(status_code=415, detail=f"Unsupported media type. Allowed types: audio/wav, audio/amr")
        content = await audio_file.read()
        if content is None:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        response = transcribe_audio_file_with_api(content, audio_file.content_type)
        return Response(content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert the given input audio file to text: {str(e)}")


@router.post("/text-to-speech", status_code=200)
async def convert_text_input_to_audio(input_text: str):
    try:
        response = synthesize_text_input_to_audio(input_text)
        return Response(content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert the given input text to audio: {str(e)}")


@router.get("/conversation", response_model=List[Conversation])
async def converse(user_id: str, last_conversations: Optional[int] = None):
    conversationList = get_conversation_list(user_id)
    return conversationList


