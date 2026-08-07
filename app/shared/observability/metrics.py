"""Prometheus metrics registry for the platform."""

from __future__ import annotations

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Histogram,
    generate_latest,
)


class PlatformMetrics:
    def __init__(self, registry: CollectorRegistry | None = None) -> None:
        self.registry = registry or CollectorRegistry()
        self.http_requests = Counter(
            "acos_ai_http_requests_total",
            "Total HTTP requests processed by the AI Platform",
            ["method", "path", "status"],
            registry=self.registry,
        )
        self.http_latency = Histogram(
            "acos_ai_http_request_duration_seconds",
            "HTTP request latency in seconds",
            ["method", "path"],
            registry=self.registry,
        )
        self.token_usage = Counter(
            "acos_ai_token_usage_total",
            "Token usage placeholder counter",
            ["provider", "model", "direction"],
            registry=self.registry,
        )
        self.estimated_cost = Counter(
            "acos_ai_estimated_cost_usd_total",
            "Estimated cost placeholder counter in USD",
            ["provider", "model"],
            registry=self.registry,
        )

    def render(self) -> tuple[bytes, str]:
        return generate_latest(self.registry), CONTENT_TYPE_LATEST


_METRICS: PlatformMetrics | None = None


def get_metrics() -> PlatformMetrics:
    global _METRICS
    if _METRICS is None:
        _METRICS = PlatformMetrics()
    return _METRICS
