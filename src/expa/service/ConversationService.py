from ..models.conversation import ConversationRequestBody, ConversationResponseBody
from ..models.starter import Starter
from ..llm import *
from ..persistence.conversation_persist import *
import datetime

from typing import Optional


logger = logging.getLogger(__name__)

def initiate_conversation(conversation_request_body: ConversationRequestBody):
    conversation_id = str(uuid.uuid4())
    print("Forming chat model")
    user_input = form_chat_model(build_initial_system_message(conversation_request_body.user_first_name, conversation_request_body.user_input), Role.USER,
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


def build_initial_system_message(user_name: str, starter_message_from_user_input: Optional[str] = None) -> str:
    try:
        base_intro = (
            f"You are an English language instructor. This is the beginning of a conversation with a beginner-level user named {user_name}. "
            f"Start with a very short and friendly greeting. Use extremely simple English. "
            f"Your goal is to help the user start speaking confidently, so ask a light question to understand their mood or interest."
        )

        if starter_message_from_user_input:
            topic_part = (
                f" Since the user selected the topic '{starter_message_from_user_input}', "
                f"mention it briefly. Say: 'Since you selected the topic \"{starter_message_from_user_input}\", let's discuss further.' "
                f"Then, start with a very short scenario or question around this topic. "
                f"Keep the language extremely simple so a beginner in English can easily understand. "
                f"Talk like a friendly colleague or a warm teacher — not too formal, and not too robotic."
            )
        else:
            topic_part = (
                " There is no specific topic provided. "
                "Start with a safe and friendly open-ended question. "
                "Ask about the user's day, feelings, or general interests. "
                "Keep it very short, soft, and beginner-friendly in English."
            )

        return base_intro + topic_part

    except Exception as e:
        return (
            f"You are an English language instructor. This is the beginning of a conversation with a beginner-level user named {user_name}. "
            f"Start with a very short and friendly greeting. There was an issue retrieving the topic information, "
            f"so begin a general but respectful conversation with a simple, light question to break the ice."
        )

