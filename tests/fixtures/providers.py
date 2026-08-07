"""Mock provider fixtures for future intelligence tests."""

from __future__ import annotations

from collections.abc import AsyncIterator

from app.intelligence.llm.ports import LlmCompletionRequest, LlmCompletionResponse, LlmPort


class MockLlmProvider(LlmPort):
    @property
    def provider_name(self) -> str:
        return "mock"

    async def complete(self, request: LlmCompletionRequest) -> LlmCompletionResponse:
        return LlmCompletionResponse(
            content="mock-response",
            model=request.model or "mock-model",
            provider=self.provider_name,
        )

    async def stream(self, request: LlmCompletionRequest) -> AsyncIterator[str]:
        yield "mock-response"

    async def health_check(self) -> bool:
        return True
