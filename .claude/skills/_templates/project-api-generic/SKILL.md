---
name: project-api-generic
description: Use when architect-stage0 needs to characterize a REST/GraphQL/gRPC API endpoint for a feature, but no specific project-api-{name}/ template matches - tier 2 for L4-API
---

# Generic API Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-api-{feature-name}/` skill when:
> - The feature exposes an API (REST / GraphQL / gRPC / WebSocket)
> - BUT no specific template exists for that feature
> - AND the AI must improvise based on graphify queries alone

The generated skill name will be `project-api-{feature-name}` (replace `{feature-name}` with the actual feature detected in `feature-elements.md`).

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-F-API-1 | Protocol (REST / GraphQL / gRPC / WebSocket) | L4 | M | `graphify query "REST GraphQL gRPC"` | `grep -rn "@RestController\|@GraphQL\|grpc\\.Server" src/ \| head` |  |
| FE-F-API-2 | Routing pattern (path-based / versioned / header-based) | L4 | M | `graphify query "request mapping route"` | `grep -rn "@RequestMapping\|router\\.\|@Path" src/ \| head` |  |
| FE-F-API-3 | Request body schema (DTO / dataclass / proto) | L4 | M | `graphify query "request body schema"` | `grep -rn "class.*Request\|@Body\|input {" src/ \| head` |  |
| FE-F-API-4 | Response body schema (envelope / direct / paginated) | L4 | M | `graphify query "response body envelope"` | `grep -rn "class.*Response\|ResponseEntity\|output {" src/ \| head` |  |
| FE-F-API-5 | Authentication requirement per endpoint | L4 | M | `graphify query "authentication required"` | `grep -rn "@PreAuthorize\|requires_auth\|@Secured" src/ \| head` |  |
| FE-F-API-6 | Error response format (RFC 7807 / custom envelope) | L4 | M | `graphify query "error response format"` | `grep -rn "@ExceptionHandler\|ProblemDetail\|@ErrorHandler" src/ \| head` |  |
| FE-F-API-7 | HTTP status code conventions (200 vs 201 vs 204) | L4 | M | `graphify query "HTTP status code"` | `grep -rn "HttpStatus\\.\|status_code\|@ResponseStatus" src/ \| head` |  |
| FE-F-API-8 | Idempotency / retry safety per verb | L4 | H | `graphify query "idempotency retry"` | `grep -rn "Idempotency-Key\|@Retryable\|safe_methods" src/ \| head` |  |
| FE-F-API-9 | Rate limit / quota policy | L4 | M | `graphify query "rate limit quota"` | `grep -rn "RateLimiter\|@RateLimit\|throttle" src/ \| head` |  |
| FE-F-API-10 | OpenAPI / schema generation | L4 | M | `graphify query "openapi schema"` | `find . -name "openapi*.json" -o -name "schema.graphql" 2>/dev/null \| head` |  |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash
4. The first investigation point determines the protocol; everything else depends on it

## Output Spec

`project-api-{feature-name}/SKILL.md` must:
- Real YAML frontmatter (`name: project-api-{feature-name}` + `description: Use when ...`)
- Replace `{feature-name}` with the actual feature name
- Sections shaped by data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`. No template rules.

## Red Flags

- Output reuses the 10-point table verbatim
- Output cites Spring `@RestController` in a non-Spring project
- Description starts with "API 接口规范" instead of "Use when"
- The `name:` field still contains the literal placeholder `{feature-name}`
