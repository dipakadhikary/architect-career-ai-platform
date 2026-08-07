"""DI wiring hooks for future orchestration implementations."""

from __future__ import annotations

from dependency_injector import containers, providers


class OrchestrationContainer(containers.DeclarativeContainer):
    """Extension container reserved for workflow/agent wiring."""

    workflow_orchestrator = providers.Object(None)
    graph_orchestrator = providers.Object(None)
    multi_agent_executor = providers.Object(None)
