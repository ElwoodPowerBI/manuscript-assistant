# Manuscript Assistant

![tests](https://github.com/ElwoodPowerBI/manuscript-assistant/actions/workflows/tests.yml/badge.svg)

A FastAPI backend service that applies large language models to publishing workflows: summarizing manuscript descriptions, extracting structured metadata, and answering questions about documents using retrieval-augmented generation.

Built against a GPT deployment in Azure AI Foundry, with embeddings from `text-embedding-3-large`.

## What it does

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Health check |
| `/summarize` | POST | Returns a two-sentence editorial summary of submitted text |
| `/extract-metadata` | POST | Returns validated structured metadata: title, genre, themes, audience |
| `/ask` | POST | Answers questions about an indexed document, grounded in retrieved passages, with sources returned |

Interactive documentation is generated automatically at `/docs` (OpenAPI 3.1).

## How it works

**Structured outputs.** `/extract-metadata` passes a Pydantic model as the response format, so the model's output is constrained to a schema and validated on arrival. The same `BookMetadata` model serves as both the LLM contract and the API response schema.

**Retrieval-augmented generation.** `/ask` splits a source document into paragraph chunks, embeds each chunk with `text-embedding-3-large`, and caches the vectors on first use. An incoming question is embedded with the same model, scored against every chunk by cosine similarity, and the top three chunks are supplied as context. The system prompt instructs the model to answer only from that context and to say it does not know otherwise, so out-of-scope questions get a refusal rather than a fabricated answer. Source passages are returned alongside the answer.

Cosine similarity is implemented directly rather than pulled from a library, to keep the retrieval math explicit and unit-testable.

**Validation at both doors.** Pydantic models validate incoming request bodies and outgoing responses. Malformed requests are rejected with a 422 before any application code runs.

## Stack

Python 3.12, FastAPI, Pydantic, uvicorn, OpenAI SDK against Azure AI Foundry, pytest, GitHub Actions.

## Running it

```bash
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1        # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
AZURE_AI_ENDPOINT=https://your-resource.services.ai.azure.com
AZURE_AI_API_KEY=your-key
AZURE_AI_DEPLOYMENT=your-deployment-name
```

`.env` is gitignored. Secrets are read from environment variables at runtime and never appear in source.

Start the server:

```bash
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/docs

## Tests

```bash
pytest -v
```

Four tests covering the health endpoint, request validation rejection, and the cosine similarity function at both ends of its range. Tests run automatically on every push via GitHub Actions.

The knowledge base loads lazily on first use rather than at import, so the test suite and CI run without network access or credentials.

## Next steps

- Replace the in-memory vector search with an Azure AI Search index using the semantic ranker
- Add PDF and DOCX ingestion with pypdf and python-docx, including chunk overlap
- Deploy to Azure Container Apps with the key in Key Vault via managed identity
- Expose the service over Model Context Protocol using FastMCP so agents can call the endpoints as tools

## Notes

Retrieval is implemented by hand here rather than delegated to a managed service. That was deliberate: understanding what vector search is doing makes it clearer when a managed index, a reranker, or a hybrid approach is the right call.