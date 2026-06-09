---
name: project-infra-security
description: Use when architect-stage0 needs to characterize the project's authentication, authorization, and security primitives - tier 1 for FE-I-006
---

# Security Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-infra-security` skill.
> Output must cite real `path/to/file:line` evidence; no template content may be copied.

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-I-006.SEC-1 | Authentication mechanism (JWT / session / OAuth2 / API key) | L1 | M | `graphify query "JWT session OAuth2"` | `grep -rn "JwtAuthenticationFilter\|@PreAuthorize\|verifyToken" src/ \| head` |  |
| FE-I-006.SEC-2 | Authorization model (RBAC / ABAC / ACL) | L1 | M | `graphify query "role based access control"` | `grep -rn "@RolesAllowed\|hasRole\|@Secured" src/ \| head` |  |
| FE-I-006.SEC-3 | Password hashing algorithm (bcrypt / argon2 / scrypt) | L1 | M | `graphify query "password hash bcrypt"` | `grep -rn "BCryptPasswordEncoder\|argon2\|hashpw" src/ \| head` |  |
| FE-I-006.SEC-4 | Secret management (Vault / env / KMS) | L1 | M | `graphify query "secret management vault"` | `grep -rn "VaultTemplate\|SecretsManager\|process.env" src/ \| head` |  |
| FE-I-006.SEC-5 | Input validation / sanitization | L1 | M | `graphify query "input validation sanitize"` | `grep -rn "@Valid\|@NotNull\|validator" src/ \| head` |  |
| FE-I-006.SEC-6 | SQL injection / XSS / CSRF defense | L1 | M | `graphify query "SQL injection XSS CSRF"` | `grep -rn "csrf\|escape\|sanitize" src/ \| head` |  |
| FE-I-006.SEC-7 | Audit logging (who-did-what-when) | L1 | M | `graphify query "audit log access"` | `grep -rn "audit\|@Audit\|accessLog" src/ \| head` |  |
| FE-I-006.SEC-8 | Sensitive data masking (PII / credentials in logs) | L1 | M | `graphify query "mask sensitive PII"` | `grep -rn "mask\|@JsonIgnore\|@Sensitive" src/ \| head` |  |
| FE-I-006.SEC-9 | Rate limiting / throttling | L1 | M | `graphify query "rate limit throttle"` | `grep -rn "RateLimiter\|@RateLimit\|Bucket4j" src/ \| head` |  |
| FE-I-006.SEC-10 | CORS / CSP / security headers | L1 | M | `graphify query "CORS CSP header"` | `grep -rn "CorsConfiguration\|@CrossOrigin\|csp" src/ \| head` |  |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash

## Output Spec

`project-infra-security/SKILL.md` must:
- Real YAML frontmatter
- Sections shaped by data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`.

## Red Flags

- Reuses this template's table verbatim
- Spring Security guidance for a non-Spring project
- Says "应该使用 BCrypt" without citing the actual encoder bean
- Description starts with "安全基础" instead of "Use when"
