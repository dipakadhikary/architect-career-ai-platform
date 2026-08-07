"""API dependency providers."""

from __future__ import annotations

from app.infrastructure.cache.redis_adapter import RedisAdapter
from app.infrastructure.vector.qdrant_adapter import QdrantAdapter
from app.shared.di.container import container
from app.shared.security.authentication import AuthenticationService


def get_redis_adapter() -> RedisAdapter:
    return container.redis_adapter()


def get_qdrant_adapter() -> QdrantAdapter:
    return container.qdrant_adapter()


def get_authentication_service() -> AuthenticationService:
    return container.authentication_service()
