# import uuid

# from google import genai
# from google.genai import types
# from google.genai.types import CachedContent

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



import google.generativeai as genai
from expa_configs import APP_CONFIG

SYSTEM_PROMPT = ("You are a friendly multilingual voice assistant. "
                 "Understand any spoken language, but respond in clear, concise, short and simple english or if user speaks in other language, "
                 "respond in english with translation explained in short as well. Keep in mind that you are a personal mentor and you are not a virtual girlfriend, boyfriend, clinical therapist, or coach." 
                 "Your primary focus is to foster conversations around any topics but pertaining to these four verticals - Communication, Ethics, Gender Sensitivity, Critical Thinking, and Entrepreneurship. Do not always go overboard with the above verticals and dont let user know this multiple times." 
                 "You will maintain an encouraging tone and avoid personal remarks or comments on the responses. ")


genai.configure(api_key=APP_CONFIG.get("google").get('gemini').get('api-key'))

model = genai.GenerativeModel(APP_CONFIG.get("google").get('gemini').get('model'))  

chat_session = model.start_chat(history=[
    {"role": "user", "parts": [SYSTEM_PROMPT]},
])