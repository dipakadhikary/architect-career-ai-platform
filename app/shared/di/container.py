"""Dependency injection application container."""

from __future__ import annotations

from dependency_injector import containers, providers

from app.infrastructure.cache.redis_adapter import RedisAdapter
from app.infrastructure.http.httpx_client import HttpxClientFactory
from app.infrastructure.knowledge.embeddings.factory import build_embedding_port
from app.infrastructure.knowledge.factory import (
    build_chunker_registry,
    build_context_builder,
    build_document_ingestion,
    build_knowledge_retriever,
    build_knowledge_service,
    build_metadata_extractor,
    build_metadata_repository,
    build_preprocessor,
    build_prompt_builder,
    build_rag_cache,
    build_rag_evaluator,
    build_response_builder,
)
from app.infrastructure.knowledge.reranking.providers import build_reranker
from app.infrastructure.knowledge.vectorstore.factory import build_vector_store
from app.infrastructure.llm.azure_openai_adapter import AzureOpenAIAdapter
from app.infrastructure.llm.factory import build_llm_port
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

    # Knowledge / Enterprise RAG
    document_ingestion = providers.Singleton(build_document_ingestion)
    preprocessor = providers.Singleton(build_preprocessor)
    metadata_extractor = providers.Singleton(build_metadata_extractor)
    metadata_repository = providers.Singleton(
        build_metadata_repository, settings=config, redis_adapter=redis_adapter
    )
    chunker_registry = providers.Singleton(build_chunker_registry)
    embedding_port = providers.Singleton(build_embedding_port, settings=config)
    vector_store = providers.Singleton(
        build_vector_store, settings=config, qdrant=qdrant_adapter
    )
    rag_cache = providers.Singleton(build_rag_cache, redis_adapter=redis_adapter)
    knowledge_retriever = providers.Singleton(
        build_knowledge_retriever,
        embeddings=embedding_port,
        store=vector_store,
        cache=rag_cache,
        metrics=metrics,
        settings=config,
    )
    knowledge_reranker = providers.Singleton(build_reranker, settings=config, metrics=metrics)
    context_builder = providers.Singleton(build_context_builder)
    prompt_builder = providers.Singleton(build_prompt_builder, settings=config)
    response_builder = providers.Singleton(build_response_builder)
    llm_port = providers.Singleton(build_llm_port, settings=config)
    rag_evaluator = providers.Singleton(build_rag_evaluator)
    knowledge_service = providers.Factory(
        build_knowledge_service,
        settings=config,
        ingestion=document_ingestion,
        preprocessor=preprocessor,
        metadata_extractor=metadata_extractor,
        metadata_repository=metadata_repository,
        chunker_registry=chunker_registry,
        embeddings=embedding_port,
        vector_store=vector_store,
        retriever=knowledge_retriever,
        reranker=knowledge_reranker,
        context_builder=context_builder,
        prompt_builder=prompt_builder,
        response_builder=response_builder,
        llm=llm_port,
        evaluator=rag_evaluator,
        metrics=metrics,
        langfuse=langfuse_adapter,
    )


def bootstrap_observability() -> None:
    configure_otel(get_settings())


container = ApplicationContainer()
