---
name: backend-django
description: Use when architect-stage0 detects a Python project using Django (including Django REST Framework) for HTTP routing, ORM, and admin - backend framework skill
---

# Django Backend Skill

> Loaded by architect-stage0 when `requirements.txt` contains `django` or `manage.py` / `settings.py` are present.
> This file is a survey questionnaire, NOT prescriptive guidance. The AI must run graphify queries and cite `path/to/file:line` for every claim.

## Investigation Points

| ID | Question | graphify query | bash fallback |
|----|----------|----------------|---------------|
| BD-1 | Which Django version and which app layout (single project vs multiple apps)? | `graphify query "django version project apps"` | `grep -rn "django" requirements.txt pyproject.toml; find . -name "apps.py" \| head` |
| BD-2 | ORM model patterns (AbstractBase / soft delete / multi-table inheritance)? | `graphify query "django model abstract base"` | `grep -rn "class.*models.Model\|class.*AbstractBase" */models.py` |
| BD-3 | DRF vs vanilla Django views (ViewSet / APIView / function-based)? | `graphify query "DRF ViewSet APIView"` | `grep -rn "ModelViewSet\|APIView\|def get\|def post" */views.py` |
| BD-4 | URL routing (include() / path() / re_path() / nested)? | `graphify query "django url include path"` | `grep -rn "urlpatterns\|include(" */urls.py` |
| BD-5 | Middleware (auth / session / CSRF / custom)? | `graphify query "django middleware"` | `grep -rn "MIDDLEWARE\|@decorator_from_middleware" settings.py */middleware.py` |
| BD-6 | Authentication (django.contrib.auth / DRF Token / JWT / OAuth)? | `graphify query "django authentication JWT"` | `grep -rn "AUTHENTICATION_BACKENDS\|JWTAuthentication\|TokenAuthentication" settings.py` |
| BD-7 | Settings structure (single settings.py / split / env-based)? | `graphify query "django settings split"` | `ls settings/ 2>/dev/null; find . -name "settings.py" -o -name "settings_*.py" \| head` |
| BD-8 | Migrations management (makemigrations / squash / data migrations)? | `graphify query "django migration"` | `find . -path "*/migrations/0*.py" -not -name "__init__.py" \| head` |
| BD-9 | Testing patterns (pytest-django / Django TestCase / factory_boy)? | `graphify query "django test pytest"` | `grep -rn "pytest-django\|TestCase\|factory" requirements.txt; find . -name "test_*.py" -o -name "tests.py" \| head` |
| BD-10 | Admin customization (ModelAdmin / list_display / actions)? | `graphify query "django admin ModelAdmin"` | `grep -rn "class.*ModelAdmin\|@admin.register" */admin.py` |

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
- Listing generic "Django best practices" not specific to the actual project
- Citing Spring/Java conventions in a Python project
- Description starting with "Django 框架调查" instead of "Use when"

## Companion Files (none)

This skill is Pattern A (self-contained). Add `scripts/` only if a detection helper is required.
