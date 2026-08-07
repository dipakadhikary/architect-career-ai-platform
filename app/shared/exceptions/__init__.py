"""Platform exception hierarchy."""

from app.shared.exceptions.base import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
    PlatformError,
    RateLimitError,
    ValidationFailedError,
)

__all__ = [
    "AuthenticationError",
    "AuthorizationError",
    "ConflictError",
    "NotFoundError",
    "PlatformError",
    "RateLimitError",
    "ValidationFailedError",
]
