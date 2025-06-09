from conversation import ConversationRequestBody, ConversationResponseBody
from ..llm import *
from ..conversation_persist import *

initial_user_input = ("This is start of the conversation with the user. You are required to initiate the conversation "
                      "understanding how are they and what they want to learn today. The logged in user name is ")


def initiate_conversation(conversation_request_body: ConversationRequestBody):
    conversation_id = str(uuid.uuid4())
    user_input = form_chat_model(initial_user_input + conversation_request_body.user_first_name, Role.USER)
    response = form_chat_model(converse_with_model([user_input]), Role.MODEL)
    response_with_embedding = generate_embedding(response)
    add_data_to_collection(form_conversation_model(conversation_id, conversation_request_body.user_first_name,
                                                   response_with_embedding))
    return ConversationResponseBody(
        model_response=response,
        conversation_id=conversation_id
    )


def form_chat_model(text: str, role: Role):
    return Chat(
        text=text,
        role=role,
        timestamp=datetime.datetime.now()
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
