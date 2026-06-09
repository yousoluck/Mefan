---
name: project-domain-generic
description: Use when architect-stage0 needs to characterize a domain entity, value object, or aggregate for a feature, but no specific project-domain-{name}/ template matches - tier 2 for L2
---

# Generic Domain Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-domain-{name}/` skill when:
> - The feature introduces a domain concept (entity / value object / aggregate / domain service)
> - BUT no specific template exists for that domain concept
> - AND the AI must improvise based on graphify queries alone

The generated skill name will be `project-domain-{name}` (replace `{name}` with the actual domain concept detected in `feature-elements.md`).

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-D-DOM-1 | Entity / value object / aggregate classification | L2 | M | `graphify query "entity aggregate value object"` | `grep -rn "@Entity\|@Aggregate\|class.*Value" src/ \| head` |  |
| FE-D-DOM-2 | Identity field and generation (UUID / auto-increment / snowflake) | L2 | M | `graphify query "identity ID generation"` | `grep -rn "@Id\|UUID\\.random\|nextId" src/ \| head` |  |
| FE-D-DOM-3 | Mutable vs immutable (frozen dataclass / builder / setters) | L2 | M | `graphify query "immutable mutable"` | `grep -rn "@dataclass(frozen\|builder\\.\\|set " src/ \| head` |  |
| FE-D-DOM-4 | Validation rules (field-level invariants) | L2 | M | `graphify query "validation invariant"` | `grep -rn "@NotNull\|@Min\|@Max\|validate" src/ \| head` |  |
| FE-D-DOM-5 | Lifecycle hooks (created/updated timestamps, soft delete) | L2 | M | `graphify query "lifecycle hook timestamp"` | `grep -rn "@PrePersist\|@CreatedDate\|deleted_at" src/ \| head` |  |
| FE-D-DOM-6 | Domain events emitted (event-driven design) | L2 | H | `graphify query "domain event publish"` | `grep -rn "ApplicationEventPublisher\|EventFired\|publishEvent" src/ \| head` |  |
| FE-D-DOM-7 | Relationships (1:N, N:M, composition vs aggregation) | L2 | M | `graphify query "relationship association"` | `grep -rn "@OneToMany\|@ManyToOne\|has_many" src/ \| head` |  |
| FE-D-DOM-8 | Equality / hashCode semantics (by-id / by-value) | L2 | H | `graphify query "equals hashCode identity"` | `grep -rn "equals\\(\\|hashCode\\(\\|__eq__" src/ \| head` |  |
| FE-D-DOM-9 | Domain service methods (verb-first naming) | L2 | M | `graphify query "domain service method"` | `grep -rn "class.*DomainService\|interface.*Domain" src/ \| head` |  |
| FE-D-DOM-10 | Persistence boundary (does it own its persistence or aggregate root only?) | L2 | H | `graphify query "aggregate root repository"` | `grep -rn "Repository<\|@Repository" src/ \| head` |  |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash

## Output Spec

`project-domain-{name}/SKILL.md` must:
- Real YAML frontmatter (`name: project-domain-{name}` + `description: Use when ...`)
- Replace `{name}` with the actual domain concept
- Sections shaped by data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`. No DDD prescriptions without project evidence.

## Red Flags

- Output reuses the 10-point table verbatim
- Output cites JPA `@Entity` in a non-Java project
- Description starts with "领域模型" instead of "Use when"
- The `name:` field still contains the literal placeholder `{name}`
