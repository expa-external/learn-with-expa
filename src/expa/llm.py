import json
import uuid
from typing import List

from google import genai
from .models.conversation import Conversation, Chat, Role
from .conversation_persist import fetch_last_updated_guardrails_for_model
from google.genai import types
from google.genai.types import CachedContent, ContentEmbedding, EmbedContentResponse
import numpy as np

# import google.generativeai as genai
from ..expa_configs import APP_CONFIG

SYSTEM_PROMPT = ("You are a friendly multilingual voice assistant. "
                 "Understand any spoken language, but respond in clear, concise, short and simple english or if user "
                 "speaks in other language,"
                 "respond in english with translation explained in short as well. Keep in mind that you are a "
                 "personal mentor and you are not a virtual girlfriend, boyfriend, clinical therapist, or coach."
                 "Your primary focus is to foster conversations around any topics but pertaining to these four "
                 "verticals - Communication, Ethics, Gender Sensitivity, Critical Thinking, and Entrepreneurship. Do "
                 "not always go overboard with the above verticals and dont let user know this multiple times."
                 "You will maintain an encouraging tone and avoid personal remarks or comments on the responses. "
                 )

api_key = 'AIzaSyCAq3W9kz6dJCGO6jF0Ee5zLBhWK6FcUpg'
chat_model = 'models/gemini-2.0-flash-001'

def converse_with_model(user_input: Chat, conversation_context: List[dict]):
    model = ModelConnection()
    prompt = {
        'role': Role.USER.value,
        'parts': [{'text': model.system_prompt}]
    }
    contents = [prompt]
    for data in conversation_context:
        contents.append({'role': 'user' if data['role'] == 'user' else 'model', 'parts': [{'text': data['text']}]})
    contents.append({
        'role': user_input.role.value,
        'parts': [{'text': user_input.text}]
    })
    print(contents)
    response = ModelConnection.client.models.generate_content(
        model=chat_model,
        contents=contents
    )
    print(response.usage_metadata)
    return response.text


def set_system_prompt_to_none():
    ModelConnection._system_prompt = None


class ModelConnection(object):
    client = None

    def __init__(self):
        self._system_prompt = None
        if ModelConnection.client is None:
            ModelConnection.client = genai.Client(api_key=api_key)

    @property
    def system_prompt(self):
        if self._system_prompt is None:
            self._system_prompt = fetch_last_updated_guardrails_for_model()
        return self._system_prompt
