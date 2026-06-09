---
name: project-infra-database
description: Use when architect-stage0 needs to characterize how the project accesses relational or document databases, including datasource configuration, ORM mapping, transaction boundaries, and query patterns - tier 1 for FE-I-001
---

# Database Access Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-infra-database` skill.
> Output must cite real `path/to/file:line` evidence from graphify queries; no template content may be copied verbatim.

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-I-001.DB-1 | Datasource configuration style (HikariCP / SQLAlchemy / pgx / mongoose / etc.) | L1 | M | `graphify query "datasource connection pool"` | `grep -rn "datasource\|DataSource" src/ \| head -20` | src/db/config.py:1-30 |
| FE-I-001.DB-2 | Transaction boundary annotation (Spring `@Transactional` / SQLAlchemy `session.begin()` / `BEGIN;COMMIT`) | L1 | M | `graphify query "transactional annotation"` | `grep -rn "@Transactional\|begin()\|BEGIN" src/ \| head -20` | src/db/session.py:1-50 |
| FE-I-001.DB-3 | ORM or query builder used (JPA / SQLAlchemy / Prisma / Drizzle / Mongoose / raw SQL) | L1 | M | `graphify query "ORM mapping entity"` | `grep -rn "@Entity\|@Table\|model\s*{" src/ \| head -20` | src/models/base.py:1-30 |
| FE-I-001.DB-4 | Schema migration tooling (Flyway / Liquibase / Alembic / Prisma migrate / knex) | L1 | M | `graphify query "schema migration"` | `find . -name "*.sql" -not -path "*/node_modules/*" \| head` | migrations/versions/0001_initial.py:1-40 |
| FE-I-001.DB-5 | Pagination pattern (offset / cursor / keyset) | L1 | M | `graphify query "pagination limit offset"` | `grep -rn "LIMIT\|OFFSET\|cursor" src/ \| head` |  |
| FE-I-001.DB-6 | Locking strategy (optimistic / pessimistic / no locks) | L1 | H | `graphify query "select for update lock"` | `grep -rn "FOR UPDATE\|@Lock\|version" src/ \| head` |  |
| FE-I-001.DB-7 | Connection pool sizing and timeout configuration | L1 | M | `graphify query "pool size connection timeout"` | `grep -rn "pool_size\|maxPoolSize\|connect_timeout" src/ \| head` | src/db/config.py:15-30 |
| FE-I-001.DB-8 | SQL injection defense (parameterized queries / ORM escaping) | L1 | M | `graphify query "parameterized query prepared statement"` | `grep -rn "String.format\|format(\".*SELECT\|concat.*SELECT" src/ \| head` |  |
| FE-I-001.DB-9 | Multi-table join patterns (JOIN / subquery / CTE) | L1 | M | `graphify query "join query subquery"` | `grep -rn "JOIN\|LEFT JOIN\|selectFrom" src/ \| head` |  |
| FE-I-001.DB-10 | Read replica routing (if any) | L1 | H | `graphify query "read replica read-only"` | `grep -rn "replica\|readOnly\|ROUTE" src/ \| head` | src/db/config.py:1-30 |
## Query Execution Rules

1. `graphify query` tokens must come from the project's actual code or `.vocab.txt` — never invent terms
2. Maximum 12 tokens per query
3. On failure, retry once with a synonym substitution, then fall back to bash

## Output Spec

The generated `project-infra-database/SKILL.md` must:
- Open with real YAML frontmatter (`name: project-infra-database` + `description: Use when ...`)
- Organize sections by what the data actually shows — DO NOT mirror the 10-point table above
- Cite each fact with `path/to/file:line`
- Mark missing data with `[需人工补充]`, never silently fabricate

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Every data point requires `path/to/file:line`. No copy-pasting from this template.

## Red Flags

- Output reuses this template's 10-point structure verbatim
- Output contains Java/Spring-specific rules when the project is Python/TypeScript
- Output says "应该使用参数化查询" (should use parameterized queries) without citing the project's actual call site
- Output's `description:` field starts with "数据库操作技能" instead of "Use when"
