from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..chat import chat_with_gemini 
from ..record_audio import record_audio_vad 
from ..transcribe_audio import transcribe_audio
import io

router = APIRouter(prefix="/converse", tags=["converse"])

@router.post("/", response_model=BaseModel)
async def converse(file: UploadFile = File(...)):

    input_audio = await file.read()
    if not isinstance(input_audio, (bytes, bytearray)):
        raise HTTPException(status_code=400, detail="Invalid file upload")

    response, elapsed_time = await chat_with_gemini(input_audio)
    return JSONResponse({
        "response": response,
        "elapsed_time": elapsed_time
    })