from conversation import ConversationRequestBody, ConversationResponseBody
from ..llm import *
from ..conversation_persist import *
import datetime

initial_user_input = ("This is start of the conversation with the user. You are required to initiate the conversation "
                      "understanding how are they and what they want to learn today. The logged in user name is ")

logger = logging.getLogger(__name__)


def initiate_conversation(conversation_request_body: ConversationRequestBody):
    conversation_id = str(uuid.uuid4())
    print("Forming chat model")
    user_input = form_chat_model(initial_user_input + conversation_request_body.user_first_name, Role.USER,
                                 conversation_id)
    print("Passing prompt to model")
    response = form_chat_model(converse_with_model(user_input, []), Role.MODEL,
                               conversation_id)
    print(response)
    print("Pushing to DB")
    add_data_to_collection(form_conversation_model(conversation_id, conversation_request_body.user_first_name, response))
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
