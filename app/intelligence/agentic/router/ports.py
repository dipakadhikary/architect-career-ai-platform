"""LLM model router port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from app.intelligence.agentic.models import RoutedModel


@dataclass(slots=True, frozen=True)
class RoutingRequest:
    capability: str
    prompt_tokens_estimate: int = 0
    prefer_low_latency: bool = False
    prefer_low_cost: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class ModelRouterPort(ABC):
    @abstractmethod
    async def route(self, request: RoutingRequest) -> RoutedModel:
        raise NotImplementedError
