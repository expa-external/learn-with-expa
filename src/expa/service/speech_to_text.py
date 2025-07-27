import base64
from google.cloud import speech_v1 as speech
from . import speech_to_text_client

def transcribe_audio_file(audio_file_content: bytes, file_type: str) -> str:
    content = base64.b64encode(audio_file_content).decode('utf-8')
    audio = speech.RecognitionAudio(content)
    encoding = speech.RecognitionConfig.AudioEncoding.AMR_WB if file_type == "audio/amr" else speech.RecognitionConfig.AudioEncoding.LINEAR16
    sample_rate = 16000 if file_type == "audio/amr" else 44100
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate,
        language_code="en-US",
        alternative_language_codes=["hi-IN", "bn-IN", "te-IN","mr-IN","ta-IN","ur-IN","gu-IN","kn-IN","ml-IN","pa-IN"],
        enable_automatic_punctuation=True,
        model="latest"
    )
    response = speech_to_text_client.client.recognize(config=config, audio=audio)
    transcript = []
    for result in response.results:
        transcript.append(result.alternatives[0].transcript)
    return " ".join(transcript)