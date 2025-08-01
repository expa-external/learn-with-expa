import datetime

from fastapi import APIRouter, HTTPException
from expa.service.ConversationService import *
from expa.persistence.guardrails_persist import *

router = APIRouter(prefix="/api/v1", tags=["Guardrails"])


@router.post("/update-guardrails")
async def update_guardrails(user_input: str, user_id: str):
    print("Received a request to update the guardrails of the model")
    updated_guardrails = UpdateGuardrails(
        version_id=str(uuid.uuid4()),
        created_by=user_id,
        created_on=datetime.datetime.now(),
        user_input=user_input
    )
    update_guardrails_for_model(updated_guardrails)
    set_system_prompt_to_none()

@router.get("/guardrails")
async def get_guardrails(user_id: str):
    try:
        guardrails_message = fetch_last_updated_guardrails_for_model()
        return guardrails_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))