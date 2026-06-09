---
name: backend-flask
description: Use when architect-stage0 detects a Python project using Flask (or Flask extensions like Flask-RESTful, Flask-Login) for HTTP routing - backend framework skill
---

# Flask Backend Skill

> Loaded by architect-stage0 when `requirements.txt` contains `flask` or `app.py` / `run.py` use `Flask(__name__)`.
> This file is a survey questionnaire, NOT prescriptive guidance. The AI must run graphify queries and cite `path/to/file:line` for every claim.

## Investigation Points

| ID | Question | graphify query | bash fallback |
|----|----------|----------------|---------------|
| BL-1 | Which Flask version and which WSGI server (gunicorn / uWSGI / waitress)? | `graphify query "Flask version gunicorn"` | `grep -rn "flask\|gunicorn" requirements.txt pyproject.toml` |
| BL-2 | Application factory pattern (create_app() vs module-level app)? | `graphify query "Flask create_app factory"` | `grep -rn "create_app\|Flask(__name__)" app.py \| head` |
| BL-3 | Blueprint organization (per resource / per feature / per layer)? | `graphify query "Flask blueprint"` | `grep -rn "Blueprint\|register_blueprint" app/ \| head` |
| BL-4 | Request lifecycle hooks (before_request / after_request / teardown)? | `graphify query "Flask before_request after_request"` | `grep -rn "@app.before_request\|@app.after_request\|teardown" app/ \| head` |
| BL-5 | Database integration (Flask-SQLAlchemy / SQLAlchemy direct / Peewee)? | `graphify query "Flask SQLAlchemy"` | `grep -rn "SQLAlchemy\|db.Model\|flask_sqlalchemy" app/ requirements.txt` |
| BL-6 | Authentication (Flask-Login / Flask-Security / JWT / custom)? | `graphify query "Flask login JWT"` | `grep -rn "LoginManager\|@login_required\|jwt" app/ \| head` |
| BL-7 | Error handling (errorhandler / abort / custom exceptions)? | `graphify query "Flask errorhandler abort"` | `grep -rn "@app.errorhandler\|abort(" app/ \| head` |
| BL-8 | Configuration management (Config classes / env vars / Flask-AppConfig)? | `graphify query "Flask config environment"` | `grep -rn "class Config\|app.config\|os.environ" app/ \| head` |
| BL-9 | Extensions registered (Flask-CORS / Flask-Migrate / Flask-Caching)? | `graphify query "Flask extension CORS"` | `grep -rn "CORS(\|Migrate(\|Cache(" app/ requirements.txt` |
| BL-10 | Testing (pytest-flask / Flask test_client / unittest)? | `graphify query "Flask test client"` | `grep -rn "pytest-flask\|test_client\|unittest" requirements.txt; find . -name "test_*.py" \| head` |

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
- Listing generic "Flask best practices" not specific to the actual project
- Citing Django/FastAPI conventions in a Flask project
- Description starting with "Flask 框架调查" instead of "Use when"

## Companion Files (none)

This skill is Pattern A (self-contained). Add `scripts/` only if a detection helper is required.
