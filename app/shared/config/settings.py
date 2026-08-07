"""Pydantic Settings for all environments."""

from __future__ import annotations

from enum import StrEnum
from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvironment(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    STAGE = "stage"
    PRODUCTION = "production"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "architect-career-ai-platform"
    app_env: AppEnvironment = AppEnvironment.DEVELOPMENT
    app_version: str = "0.1.0"
    app_debug: bool = False
    app_host: str = "0.0.0.0"
    app_port: int = 8090

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_json: bool = True

    cors_allow_origins: str = "*"
    rate_limit_requests_per_minute: int = 120

    auth_jwt_enabled: bool = False
    auth_jwt_secret: SecretStr = SecretStr("change-me")
    auth_jwt_algorithm: str = "HS256"
    auth_jwt_audience: str = ""
    auth_jwt_issuer: str = ""
    auth_api_key_enabled: bool = False
    auth_api_keys: str = ""
    auth_internal_service_header: str = "X-Internal-Service"
    auth_internal_service_tokens: str = ""

    redis_url: str = "redis://localhost:6379/0"
    redis_enabled: bool = True

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: SecretStr | None = None
    qdrant_enabled: bool = True

    openai_api_key: SecretStr | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_default_model: str = "gpt-4o-mini"
    openai_enabled: bool = False

    azure_openai_api_key: SecretStr | None = None
    azure_openai_endpoint: str = ""
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_deployment: str = ""
    azure_openai_enabled: bool = False

    ollama_base_url: str = "http://localhost:11434"
    ollama_default_model: str = "llama3.2"
    ollama_enabled: bool = False

    llm_provider: Literal["openai", "azure_openai", "ollama"] = "openai"

    langfuse_public_key: str = ""
    langfuse_secret_key: SecretStr | None = None
    langfuse_host: str = "https://cloud.langfuse.com"
    langfuse_enabled: bool = False

    otel_enabled: bool = True
    otel_service_name: str = "architect-career-ai-platform"
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    otel_traces_sampler_arg: float = Field(default=1.0, ge=0.0, le=1.0)

    metrics_enabled: bool = True

    @field_validator("app_env", mode="before")
    @classmethod
    def normalize_env(cls, value: object) -> object:
        if isinstance(value, str):
            return value.lower()
        return value

    @property
    def cors_origins(self) -> list[str]:
        if self.cors_allow_origins.strip() == "*":
            return ["*"]
        return [item.strip() for item in self.cors_allow_origins.split(",") if item.strip()]

    @property
    def api_key_set(self) -> set[str]:
        return {item.strip() for item in self.auth_api_keys.split(",") if item.strip()}

    @property
    def internal_service_token_set(self) -> set[str]:
        return {
            item.strip() for item in self.auth_internal_service_tokens.split(",") if item.strip()
        }

    @property
    def is_production(self) -> bool:
        return self.app_env == AppEnvironment.PRODUCTION


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()
