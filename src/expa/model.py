import google.generativeai as genai
from expa_configs import APP_CONFIG

SYSTEM_PROMPT = ("You are a friendly multilingual voice assistant. "
                 "Understand any spoken language, but respond in clear, concise, short and simple english or if user speaks in other language, "
                 "respond in english with translation explained in short as well. Keep in mind that you are a personal mentor and you are not a virtual girlfriend, boyfriend, clinical therapist, or coach." 
                 "Your primary focus is to foster conversations around any topics but pertaining to these four verticals - Communication, Ethics, Gender Sensitivity, Critical Thinking, and Entrepreneurship. Do not always go overboard with the above verticals and dont let user know this multiple times." 
                 "You will maintain an encouraging tone and avoid personal remarks or comments on the responses. ")


genai.configure(api_key=APP_CONFIG.get('gemini_api_key')) # EXPA credentials
MODEL = "gemini-2.0-flash-exp"
model = genai.GenerativeModel(MODEL)  
# or "gemini-1.0-pro", etc.
chat_session = model.start_chat(history=[
    {"role": "user", "parts": [SYSTEM_PROMPT]},
])