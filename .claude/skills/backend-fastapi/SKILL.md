---
name: backend-fastapi
description: Use when architect-stage0 detects a Python project using FastAPI for HTTP routing, dependency injection, and async request handling - backend framework skill
---

# FastAPI Backend Skill

> Loaded by architect-stage0 when `requirements.txt` contains `fastapi` or `main.py` / `app.py` use `FastAPI()`.
> This file is a survey questionnaire, NOT prescriptive guidance. The AI must run graphify queries and cite `path/to/file:line` for every claim.

## Investigation Points

| ID | Question | graphify query | bash fallback |
|----|----------|----------------|---------------|
| BF-1 | Which FastAPI version and which ASGI server (uvicorn / hypercorn / gunicorn)? | `graphify query "FastAPI version uvicorn"` | `grep -rn "fastapi\|uvicorn" requirements.txt pyproject.toml` |
| BF-2 | Route organization (APIRouter per resource / single module / include_router chains)? | `graphify query "APIRouter include_router"` | `grep -rn "APIRouter\|include_router" app/ main.py` |
| BF-3 | Dependency injection pattern (`Depends(...)` factories, `Annotated`)? | `graphify query "Depends dependency"` | `grep -rn "Depends(\|Annotated\[" app/ main.py` |
| BF-4 | Pydantic model layering (BaseModel / schemas per resource / nested)? | `graphify query "Pydantic BaseModel schema"` | `grep -rn "class.*BaseModel\|class.*Schema" app/ schemas/` |
| BF-5 | Async vs sync handler style (async def / def with threadpool)? | `graphify query "async def sync handler"` | `grep -rn "async def\|def " app/ --include="*.py" \| head` |
| BF-6 | Authentication / authorization (OAuth2 / JWT / APIKeyHeader / HTTPBearer)? | `graphify query "OAuth2 JWT security"` | `grep -rn "OAuth2PasswordBearer\|HTTPBearer\|jwt" app/ \| head` |
| BF-7 | Middleware (CORS / GZip / request-id / logging)? | `graphify query "middleware CORS"` | `grep -rn "add_middleware\|@app.middleware" app/ main.py` |
| BF-8 | Error handling (HTTPException / custom handlers / validation error response)? | `graphify query "HTTPException handler"` | `grep -rn "HTTPException\|exception_handler" app/ \| head` |
| BF-9 | Background tasks (BackgroundTasks / Celery / arq)? | `graphify query "background task"` | `grep -rn "BackgroundTasks\|@celery\|arq" app/ \| head` |
| BF-10 | OpenAPI schema customization (tags / description / examples)? | `graphify query "openapi tags schema"` | `grep -rn "openapi_tags\|FastAPI(\|description=" app/ main.py` |

## Output Requirements

When architect-stage0 fills this in:

1. Real YAML frontmatter (`---` block, `name` + `description: Use when ...`)
2. Sections shaped by the actual data — do NOT mirror the 10-question table above
3. Every claim cited with `path/to/file:line`
4. Missing data → `[需人工补充]`, never silent fabrication

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`.

## Red Flags

- Reusing the 10-question table verbatim as the output structure
- Listing generic "FastAPI best practices" not specific to the actual project
- Citing Spring/Java conventions in a Python project
- Description starting with "FastAPI 框架调查" instead of "Use when"

## Companion Files (none)

This skill is Pattern A (self-contained). Add `scripts/` only if a detection helper is required.
