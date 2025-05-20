# Send audio file to Gemini and receive text response
import time
import subprocess
from gtts import gTTS
from .model import chat_session
import asyncio

async def chat_with_gemini(audio_data: bytes):
    start = time.time()

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