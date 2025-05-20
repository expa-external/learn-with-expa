# Send audio file to Gemini and receive text response
import time
import subprocess
from gtts import gTTS
from .model import chat_session
import asyncio

async def chat_with_gemini(audio_file: bytes):
    start = time.time()
    # with open(audio_file, "rb") as f:
    #     audio_data = f.read()

    # audio_data = await streaming_response_to_bytes_sync(audio_file)
    audio_data = audio_file

    # Create a Part with audio data
    audio_part = {
        "mime_type": "audio/wav",  # or audio/mpeg, etc.
        "data": audio_data,
    }

    # Send audio message to chat
    response = chat_session.send_message(audio_part)
    end = time.time()

    elapsed_time = end - start
    print(f"\nGemini response time: {elapsed_time:.2f} seconds")
    return response._result.candidates[0].content.parts[0].text, elapsed_time

# Convert text to speech and play using Mac native audio player
def speak(text, filename="response.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    subprocess.run(["afplay", filename]) # For Mac. Use "start" on Windows, "aplay" on Linux


async def streaming_response_to_bytes(streaming_response):
    content = b""
    async for chunk in streaming_response.body_iterator:
        content += chunk
    return content

def streaming_response_to_bytes_sync(sr) -> bytes:
    """
    Synchronously drains a FastAPI/Starlette StreamingResponse
    and returns its full body as bytes.
    """
    async def _drain() -> bytes:
        data = b""
        async for chunk in sr.body_iterator:
            data += chunk
        return data

    # Create a fresh event loop so we don't collide with any running loop
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(_drain())
    finally:
        loop.close()
    # # This spins up a one-off event loop to await the coroutine.
    # return asyncio.run(streaming_response_to_bytes(sr))