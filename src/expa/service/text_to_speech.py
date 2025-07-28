from google.cloud import texttospeech
from . import text_to_speech_client
import logging

logger = logging.getLogger(__name__)

def convert_text_to_speech(text_input: str) -> bytes:
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text_input)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-IN",
            name="en-IN-Standard-A",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding= texttospeech.AudioEncoding.MP3
        )
        response = text_to_speech_client.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        return response.audio_content
    except Exception as e:
        logger.error("Error while converting text to audio", e)
        raise e