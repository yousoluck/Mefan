---
name: project-service-generic
description: Use when architect-stage0 needs to characterize an application-layer use-case service, but no specific project-service-{name}/ template matches - tier 2 for L3
---

# Generic Service Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-service-{feature-name}/` skill when:
> - The feature introduces a use-case service (application-layer orchestration)
> - BUT no specific template exists for that service
> - AND the AI must improvise based on graphify queries alone

The generated skill name will be `project-service-{feature-name}` (replace `{feature-name}` with the actual use case).

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-A-SVC-1 | Service class naming and suffix (Service / UseCase / Handler / Command) | L3 | M | `graphify query "service use case handler"` | `grep -rn "class.*Service\|class.*UseCase\|class.*Handler" src/ \| head` |  |
| FE-A-SVC-2 | Method granularity (CRUD-per-method vs single-execute) | L3 | M | `graphify query "service method granularity"` | `grep -rn "public.*create\|public.*update\|public.*delete" src/ \| head` |  |
| FE-A-SVC-3 | Transaction boundary (where it starts, where it ends) | L3 | M | `graphify query "transaction boundary"` | `grep -rn "@Transactional\|session\\.begin" src/ \| head` |  |
| FE-A-SVC-4 | Dependency injection pattern (constructor / field / setter) | L3 | M | `graphify query "dependency injection constructor"` | `grep -rn "@Autowired\|@Inject\|constructor" src/ \| head` |  |
| FE-A-SVC-5 | Error handling / exception translation | L3 | M | `graphify query "exception translation"` | `grep -rn "throw new\|raise \|catch.*Exception" src/ \| head` |  |
| FE-A-SVC-6 | Logging entry/exit and key params | L3 | M | `graphify query "logging entry exit"` | `grep -rn "logger\\.info\|log\\.info\|@Log" src/ \| head` |  |
| FE-A-SVC-7 | Validation at the boundary (input sanitization) | L3 | M | `graphify query "input validation boundary"` | `grep -rn "@Valid\|validate\\(\\|check" src/ \| head` |  |
| FE-A-SVC-8 | External API call pattern (sync / async / circuit-breaker) | L3 | H | `graphify query "external API call"` | `grep -rn "RestTemplate\|HttpClient\|axios\\.\\|resilience" src/ \| head` |  |
| FE-A-SVC-9 | Idempotency key handling for write operations | L3 | H | `graphify query "idempotency key"` | `grep -rn "Idempotency-Key\|idempotency_key" src/ \| head` |  |
| FE-A-SVC-10 | Event publication (outbox pattern? direct publish?) | L3 | H | `graphify query "event publish outbox"` | `grep -rn "Outbox\|publishEvent\|emit" src/ \| head` |  |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash

## Output Spec

`project-service-{feature-name}/SKILL.md` must:
- Real YAML frontmatter
- Replace `{feature-name}` with the actual use case
- Sections shaped by data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`. No "should" without a citation.

## Red Flags

- Output reuses the 10-point table verbatim
- Output prescribes a specific framework's service style (e.g. Spring `@Service`) for a non-Spring project
- Description starts with "服务层" instead of "Use when"
- The `name:` field still contains the literal placeholder `{feature-name}`
