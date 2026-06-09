---
name: project-feature-generic
description: Use when architect-stage0 needs to characterize a cross-layer business scenario (BS-* in feature-elements.md), but no specific project-feature-{name}/ template matches - tier 2 for L5
---

# Generic Business Scenario Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-feature-{name}/` skill when:
> - The feature spans L1-L4 (a complete business scenario, BS-*)
> - BUT no specific template exists for that scenario
> - AND the AI must improvise based on graphify queries alone

The generated skill name will be `project-feature-{name}` (replace `{name}` with the actual scenario detected in `feature-elements.md`).

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-BS-FEAT-1 | Entry point (API endpoint / UI button / scheduled job / event listener) | L5 | M | `graphify query "entry point trigger"` | `grep -rn "@PostMapping\|onClick\|@Scheduled\|@EventListener" src/ \| head` |  |
| FE-BS-FEAT-2 | Cross-layer flow (UI → API → Service → Domain → Infra) | L5 | H | `graphify query "layer flow call chain"` | `graphify path "Controller" "Repository"` |  |
| FE-BS-FEAT-3 | State machine (initial → intermediate → terminal states) | L5 | H | `graphify query "state machine transition"` | `grep -rn "enum.*Status\|state.*transition\|from.*to" src/ \| head` |  |
| FE-BS-FEAT-4 | Business rules / invariants enforced | L5 | H | `graphify query "business rule invariant"` | `grep -rn "assert\|require\|throw.*Exception\|Invariant" src/ \| head` |  |
| FE-BS-FEAT-5 | External integrations (3rd party APIs, payment, email) | L5 | M | `graphify query "external integration"` | `grep -rn "HttpClient\|stripe\\.\\|sendgrid\|twilio" src/ \| head` |  |
| FE-BS-FEAT-6 | Compensation / rollback on partial failure | L5 | H | `graphify query "compensation rollback"` | `grep -rn "saga\|compensate\|rollback" src/ \| head` |  |
| FE-BS-FEAT-7 | Side effects (notifications, audit, metrics) | L5 | M | `graphify query "side effect notification"` | `grep -rn "notification\|audit\|metric\\.increment" src/ \| head` |  |
| FE-BS-FEAT-8 | Failure modes and how the scenario handles them | L5 | H | `graphify query "failure mode handling"` | `grep -rn "catch.*Exception\|onError\|fallback" src/ \| head` |  |
| FE-BS-FEAT-9 | Test coverage (unit / integration / e2e) | L5 | M | `graphify query "test coverage"` | `find . -name "*test*" -o -name "*spec*" 2>/dev/null \| grep -v node_modules \| head` |  |
| FE-BS-FEAT-10 | Observability (tracing, logs, alerts for this flow) | L5 | M | `graphify query "observability trace log"` | `grep -rn "traceId\|logger\\.info.*scenario\|alert" src/ \| head` |  |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash
4. Use `graphify path "Entry" "Exit"` to trace cross-layer flow when available

## Output Spec

`project-feature-{name}/SKILL.md` must:
- Real YAML frontmatter
- Replace `{name}` with the actual scenario
- Sections shaped by data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`. Cross-layer flows MUST use `graphify path` for evidence, not assumptions.

## Red Flags

- Output reuses the 10-point table verbatim
- Output describes the scenario without any cross-layer flow evidence
- Description starts with "业务流程" instead of "Use when"
- The `name:` field still contains the literal placeholder `{name}`
