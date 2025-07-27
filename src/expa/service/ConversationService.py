from ..models.conversation import ConversationRequestBody, ConversationResponseBody
from ..models.theme import Theme
from ..llm import *
from .speech_to_text import *
from .text_to_speech import *
from ..persistence.conversation_persist import *
from ..persistence.theme_persist import *
import datetime

from typing import Optional


logger = logging.getLogger(__name__)

# initial_user_input = ("This is start of the conversation with the user. You are required to initiate the conversation with the very short greetings"
#                       " and understanding what is the user mindset. The logged in user name is {}. "
#                     theme != null then " The user want to have a discussion around the topic {} and please start the conversation around the same topic. A little bit of deviation is fine but revolve the conversation around the idea if maybe not the same scenario." 
#                     " Let the conversation starter be around that topic and short starter.")


def initiate_conversation(conversation_request_body: ConversationRequestBody):
    conversation_id = str(uuid.uuid4())
    print("Forming chat model")
    user_input = form_chat_model(build_initial_system_message(conversation_request_body.user_first_name, conversation_request_body.topic_id), Role.USER,
                                 conversation_id)
    print("Passing prompt to model")
    response = form_chat_model(converse_with_model(user_input, []), Role.MODEL,
                               conversation_id)
    print(response)

    print("Pushing to DB")
    add_data_to_collection(form_conversation_model(conversation_id, conversation_request_body.user_id, response))
    return ConversationResponseBody(
        model_response=response.text,
        conversation_id=conversation_id
    )


def continue_conversation(conversation_request_body: ConversationRequestBody):
    print("Form chat model from the user input")
    user_input = form_chat_model(conversation_request_body.user_input, Role.USER,
                                 conversation_request_body.conversation_id)
    print("Fetch last 10 conversations between the chat and model")
    conversational_context = fetch_last_k_conversation(conversation_request_body.conversation_id, 10)
    print(conversational_context)
    model_response = form_chat_model(converse_with_model(user_input, conversational_context), Role.MODEL,
                                     conversation_request_body.conversation_id)
    print("Persist data to collection")
    update_data_to_collection([user_input.model_dump(), model_response.model_dump()], conversation_request_body.conversation_id)
    return ConversationResponseBody(
        model_response=model_response.text,
        conversation_id=conversation_request_body.conversation_id
    )

def end_conversation(conversation_request_body: ConversationRequestBody):
    print("Received a request to end the conversation")
    update_summary_after_completion(conversation_request_body.conversation_id)
    return ConversationResponseBody()


def transcribe_audio_file_with_api(audio_file: bytes, file_type: str):
    return transcribe_audio_file(audio_file_content=audio_file, file_type=file_type)

def synthesize_text_input_to_audio(text_input: str):
    return convert_text_to_speech(text_input)


def update_guardrails_for_model_based_on_input(user_input: str, user_id: str):
    print("Received a request to update the guardrails of the model")
    updated_guardrails = UpdateGuardrails(
        version_id=str(uuid.uuid4()),
        created_by=user_id,
        created_on=datetime.datetime.now(),
        user_input=user_input
    )
    update_guardrails_for_model(updated_guardrails)
    set_system_prompt_to_none()


def form_chat_model(text: str, role: Role, conversationId: str):
    return Chat(
        text=text,
        role=role,
        timestamp=datetime.datetime.now(),
        conversationId=conversationId
    )


def form_conversation_model(conversation_id: str, first_name: str, chat: Chat):
    return Conversation(
        conversation_id=conversation_id,
        conversation_state='ACTIVE',
        user_id=first_name,
        creation_ts=datetime.datetime.now(),
        updated_ts=datetime.datetime.now(),
        chat_history=[chat]
    )


def build_initial_system_message(user_name: str, topic_id: Optional[str] = None) -> str:
    try:
        base_intro = (
            f"This is the start of the conversation with the user. "
            f"You are required to initiate the conversation with very short greetings "
            f"and try to understand the user's mindset. The logged-in user name is {user_name}."
        )

        if topic_id:
            theme = get_theme_by_topic_id(topic_id)
            print(theme)
        else:
            theme = None

        if theme:
            topic_part = (
                f" The user wants to have a discussion around the topic '{theme['name']}'. "
                f"Please start the conversation around this topic. A little deviation is fine, "
                f"but try to revolve the conversation around the idea: '{theme['short_description']}', even if not the same scenario. "
                f"Let the conversation starter be brief and theme-driven."
            )
        else:
            topic_part = (
                " There is no specific topic provided. Start an open-ended but ethically safe and socially appropriate conversation. "
                "Ask light questions to understand the user's interests or mood. Be respectful and friendly."
            )

        return base_intro + topic_part

    except Exception as e:
        return (
            f"This is the start of the conversation with the user. "
            f"You are required to initiate the conversation with very short greetings and try to understand the user's mindset. "
            f"The logged-in user name is {user_name}. "
            f"There was an issue retrieving the topic information, so start a general but ethical and respectful conversation."
        )

