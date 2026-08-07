# ACOS AI Platform

Reusable, **domain-agnostic** AI Platform foundation for the Architect Career Operating System.

Business domains (Career, Learning, Knowledge, Portfolio) consume this platform. They do not live inside it.

## What this repository is

- FastAPI platform foundation on Clean Architecture
- Contract-driven APIs via `architect-career-ai-contracts`
- Enterprise Knowledge RAG capability (replaceable adapters per layer)
- Ports/adapters for LLM, embeddings, retrieval, memory, and tools
- Observability, security preparation, DI, Docker, and quality tooling

## What this repository is not

- Not a CRUD app
- Not Career/Learning/Portfolio domain business logic
- Not a LangChain/Qdrant/OpenAI-locked demo

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload --port 8090
```

Health and Knowledge:

- `GET /api/v1/ai/health` (contract model)
- `POST /api/v1/ai/knowledge/index`
- `POST /api/v1/ai/knowledge/search`
- `POST /api/v1/ai/knowledge/summarize`
- `GET /api/v1/system/liveness`
- `GET /api/v1/system/readiness`
- `GET /api/v1/system/metrics`
- OpenAPI: `/docs`

## Sync contracts

```bash
python scripts/sync_contracts.py
pip install -e ./third_party/acos_ai_contracts
```

## Docker

```bash
docker compose -f docker-compose.dev.yml up --build
```

## Documentation

- [Architecture overview](docs/architecture-overview.md)
- [Layer responsibilities](docs/layer-responsibilities.md)
- [Dependency rules](docs/dependency-rules.md)
- [Coding standards](docs/coding-standards.md)
- [How to add an LLM provider](docs/how-to-add-llm-provider.md)
- [How to add a retriever](docs/how-to-add-retriever.md)
- [How to add an agent](docs/how-to-add-agent.md)
- [How to add a tool](docs/how-to-add-tool.md)
- [Development guide](docs/development-guide.md)
