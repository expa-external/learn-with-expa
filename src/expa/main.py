
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from pydub import AudioSegment
import io
from .chat import chat_with_gemini
from .record_audio import record_audio_vad
from .transcribe_audio import transcribe_audio
import requests

def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def root():
        response = {"Hello": "World"}
        return JSONResponse(response)

    @app.post("/converse")
    async def converse(file: UploadFile = File(...)):
        # Read uploaded audio into memory
        input_audio = await file.read()

        # # Use BytesIO to simulate file-like object
        # input_stream = io.BytesIO(input_audio)

        # # Guess format from filename
        # input_format = file.filename.split('.')[-1].lower()

        # try:
        #     # Convert to WAV using pydub
        #     audio = AudioSegment.from_file(input_stream, format=input_format)
        # except Exception as e:
        #     return {"error": f"Could not process the audio file: {str(e)}"}

        # # Export to WAV format in memory
        # output_buffer = io.BytesIO()
        # audio.export(output_buffer, format="wav")
        # output_buffer.seek(0)

        # # Return the file as a streaming response
        # # wav_file = StreamingResponse(output_buffer, media_type="audio/wav", headers={
        # #     "Content-Disposition": f"attachment; filename=converted.wav"
        # # })

        # # wav_file is bytes
        # wav_file: bytes = output_buffer.getvalue()

        # transcript = transcribe_audio(wav_file)
        # print(f"Audio preview: {transcript}")

        # Audio to Text with Gemini
        response, elapsed_time = await chat_with_gemini(input_audio)

        # Convert the Protobuf message into a plain dict
        # resp_dict = MessageToDict(proto_response)

        return {
            "response": response,
            "elapsed_time": elapsed_time
        }

        # return {"response": response, "elapsed_time": elapsed_time }


        # print("Gemini says:\n")
        # reply = ""
        # for chunk in response:
        #     reply += chunk.text + " "
        # print(reply)

        # Text to Speech
        # speak(reply)
        # time.sleep(1)
        # print("\n--- Say something else ---\n")
    
    return app


if __name__ == "__main__":
    print("Say something... (say 'exit' to quit)\n")
    fileName = record_audio_vad()
    with open(fileName , "rb") as f:
        response = requests.post("http://localhost:8000/converse", files={"file": (fileName, f, "audio/wav")})
        # print(response.json())
        # print(response)
        reply = ""
        for chunk in response.json():
            reply += chunk.text + " "
        print(reply)