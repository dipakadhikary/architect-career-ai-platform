"""Contract-aligned Chat AI endpoint (agentic orchestration)."""

from __future__ import annotations

from acos_ai_contracts.models.chat_completion_request import ChatCompletionRequest
from acos_ai_contracts.models.chat_completion_response import ChatCompletionResponse
from fastapi import APIRouter, Depends

from app.api.dependencies import get_agentic_service
from app.orchestration.agentic.service import AgenticOrchestrationService

router = APIRouter(tags=["Chat AI"])


@router.post(
    "/api/v1/ai/chat/completions",
    response_model=ChatCompletionResponse,
    response_model_by_alias=True,
    summary="Create chat completion",
)
async def create_chat_completion(
    body: ChatCompletionRequest,
    service: AgenticOrchestrationService = Depends(get_agentic_service),
) -> ChatCompletionResponse:
    history = None
    if body.history:
        history = [{"role": item.role, "content": item.content} for item in body.history]
    result = await service.chat_completion(
        user_id=body.user_id,
        message=body.message,
        conversation_id=body.conversation_id,
        history=history,
    )
    return ChatCompletionResponse(
        conversationId=str(result["conversation_id"]),
        message=str(result["message"]),
        model=result.get("model"),
    )
