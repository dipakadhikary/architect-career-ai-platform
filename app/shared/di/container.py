"""Dependency injection application container."""

from __future__ import annotations

from dependency_injector import containers, providers

from app.infrastructure.cache.redis_adapter import RedisAdapter
from app.infrastructure.http.httpx_client import HttpxClientFactory
from app.infrastructure.llm.azure_openai_adapter import AzureOpenAIAdapter
from app.infrastructure.llm.ollama_adapter import OllamaAdapter
from app.infrastructure.llm.openai_adapter import OpenAIAdapter
from app.infrastructure.observability.langfuse_adapter import LangfuseAdapter
from app.infrastructure.observability.otel import configure_otel
from app.infrastructure.storage.filesystem_adapter import FilesystemAdapter
from app.infrastructure.vector.qdrant_adapter import QdrantAdapter
from app.shared.config.settings import get_settings
from app.shared.observability.metrics import get_metrics
from app.shared.security.authentication import AuthenticationService


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Singleton(get_settings)
    metrics = providers.Singleton(get_metrics)
    authentication_service = providers.Factory(AuthenticationService, settings=config)
    http_client_factory = providers.Singleton(HttpxClientFactory, settings=config)
    redis_adapter = providers.Singleton(RedisAdapter, settings=config)
    qdrant_adapter = providers.Singleton(QdrantAdapter, settings=config)
    filesystem_adapter = providers.Singleton(FilesystemAdapter)
    langfuse_adapter = providers.Singleton(LangfuseAdapter, settings=config)
    openai_adapter = providers.Singleton(OpenAIAdapter, settings=config)
    azure_openai_adapter = providers.Singleton(AzureOpenAIAdapter, settings=config)
    ollama_adapter = providers.Singleton(OllamaAdapter, settings=config)


def bootstrap_observability() -> None:
    configure_otel(get_settings())


container = ApplicationContainer()
