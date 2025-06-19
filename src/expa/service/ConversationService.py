from conversation import ConversationRequestBody, ConversationResponseBody
from ..llm import *
from ..conversation_persist import *
import datetime

initial_user_input = ("This is start of the conversation with the user. You are required to initiate the conversation "
                      "understanding how are they and what they want to learn today. The logged in user name is ")

logger = logging.getLogger(__name__)


def initiate_conversation(conversation_request_body: ConversationRequestBody):
    conversation_id = str(uuid.uuid4())
    user_name = conversation_request_body.user_first_name
    print("Forming chat model")
    user_input = form_chat_model(initial_user_input + conversation_request_body.user_first_name, Role.USER,
                                 conversation_id)
    print("Passing prompt to model")
    response = form_chat_model(converse_with_model(user_input, []), Role.MODEL,
                               conversation_id)
    print(response)
    print("Generate Embedding")
    response_with_embedding = generate_embedding(response)
    print(response_with_embedding)
    print("Pushing to DB")
    add_data_to_collection(form_conversation_model(conversation_id, conversation_request_body.user_first_name), response_with_embedding)
    return ConversationResponseBody(
        model_response=response.text,
        conversation_id=conversation_id
    )


def continue_conversation(conversation_request_body: ConversationRequestBody):
    print("Form chat model from the user input")
    user_input = form_chat_model(conversation_request_body.user_input, Role.USER,
                                 conversation_request_body.conversation_id)
    print("Generate embeddings for the input")
    user_input_with_embedding = generate_embedding(user_input)
    print("Updating the firestore conversation with the latest user input")
    update_data_to_collection(user_input_with_embedding)
    print("Retrieve context from firestore using the user embeddings.")
    conversational_context = retrieve_context_from_embeddings(user_input_with_embedding,
                                                              conversation_request_body.conversation_id, k=100)
    model_response = form_chat_model(converse_with_model(user_input, conversational_context), Role.MODEL,
                                     conversation_request_body.conversation_id)
    print("Generate embedding of model response")
    model_response_with_embedding = generate_embedding(model_response)
    print("Persist data to collection")
    update_data_to_collection(model_response_with_embedding)
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


def form_conversation_model(conversation_id: str, first_name: str):
    return Conversation(
        conversation_id=conversation_id,
        conversation_state='ACTIVE',
        user_id=first_name,
        creation_ts=datetime.datetime.now(),
        updated_ts=datetime.datetime.now()
    )
