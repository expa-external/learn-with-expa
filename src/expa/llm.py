import json
import uuid
from typing import List

from google import genai
from .models.conversation import Conversation, Chat, Role
from google.genai import types
from google.genai.types import CachedContent, ContentEmbedding, EmbedContentResponse
import numpy as np

# # from expa_configs import APP_CONFIG

# SYSTEM_PROMPT = ("You are a friendly multilingual voice assistant. "
#                  "Understand any spoken language, but respond in clear, concise, short and simple english or if user "
#                  "speaks in other language,"
#                  "respond in english with translation explained in short as well. Keep in mind that you are a "
#                  "personal mentor and you are not a virtual girlfriend, boyfriend, clinical therapist, or coach."
#                  "Your primary focus is to foster conversations around any topics but pertaining to these four "
#                  "verticals - Communication, Ethics, Gender Sensitivity, Critical Thinking, and Entrepreneurship. Do "
#                  "not always go overboard with the above verticals and dont let user know this multiple times."
#                  "You will maintain an encouraging tone and avoid personal remarks or comments on the responses. ")

# api_key = ''
# model = 'models/gemini-2.0-flash-001'
# client = genai.Client()


# def initiateClient(conversation_id: uuid):
#     # Creating a cache to store the context for 1 hour as of now.
#     cache = client.caches.create(
#         model=model,
#         config=types.CreateCachedContentConfig(
#             display_name=conversation_id,
#             system_instruction=SYSTEM_PROMPT
#         )
#     )
#     return cache


# def initiateConversation(cache: CachedContent, user_input: str):
#     response = client.models.generate_content(
#         model=model,
#         contents=user_input,
#         config=types.GenerateContentConfig(cached_content=cache.name)
#     )
#     print(response.usage_metadata)
#     return response.text


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
embedding_model = 'models/text-embedding-004'


# genai.configure(api_key=APP_CONFIG.get("google").get('gemini').get('api-key'))
# def initiateCache(conversation_id: str):
#     # Creating a cache to store the context for 1 hour as of now.
#     cache = ModelConnection.client.caches.create(
#         model=model,
#         config=types.CreateCachedContentConfig(
#             display_name=conversation_id,
#             system_instruction=SYSTEM_PROMPT
#         )
#     )
#     print(f'{cache=}')


def converse_with_model(user_input: Chat, conversation_context: List[dict]):
    prompt = {
        'role': Role.USER.value,
        'parts': [{'text': SYSTEM_PROMPT}]
    }
    contents = [prompt]
    for data in conversation_context:
        contents.append({'role': 'user' if data['speaker'] == 'user' else 'model', 'parts': [{'text': data['text']}]})
    contents.append({
        'role': user_input.role.value,
        'parts': [{'text': user_input.text}]
    })
    response = ModelConnection.client.models.generate_content(
        model=chat_model,
        contents=contents
    )
    print(response.usage_metadata)
    return response.text


def generate_embedding(chat: Chat):
    result = ModelConnection.client.models.embed_content(
        model=embedding_model,
        contents=chat.text,
        config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
    )
    chat.embedding = unit_normalize_the_chat_embedding(result)
    return chat


def unit_normalize_the_chat_embedding(embeddingResponse: EmbedContentResponse):
    embedded_values = embeddingResponse.embeddings.pop().values
    print(embedded_values)
    embedding_array = np.array(embedded_values)
    norm = np.linalg.norm(embedding_array)
    if norm == 0:
        return embedded_values
    normalised_array = embedding_array / norm
    return normalised_array.tolist()


class ModelConnection(object):
    client = None

    def __init__(self):
        if ModelConnection.client is None:
            ModelConnection.client = genai.Client(api_key=api_key)
