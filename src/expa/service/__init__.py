from google.cloud import speech_v1 as speech
from google.cloud import texttospeech
import logging

logger = logging.getLogger(__name__)

class SpeechToText(object):
    client = None

    def __init__(self):
        if SpeechToText.client is None:
            SpeechToText.client = speech.SpeechClient()


class TextToSpeech(object):
    client = None

    def __init__(self):
        if TextToSpeech.client is None:
            TextToSpeech.client = texttospeech.TextToSpeechClient()
            logger.info("Google Cloud Text-to-Speech client initialized.")

text_to_speech_client = TextToSpeech()
speech_to_text_client = SpeechToText()