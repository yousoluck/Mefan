---
name: project-infra-network
description: Use when architect-stage0 needs to characterize how the project makes outbound HTTP/TCP calls to remote services - tier 1 for FE-I-004
---

# Network Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-infra-network` skill.
> Output must cite real `path/to/file:line` evidence; no template content may be copied.

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-I-004.NET-1 | HTTP client library (OkHttp / HttpClient / axios / requests / fetch) | L1 | M | `graphify query "http client library"` | `grep -rn "OkHttpClient\|HttpClient\|axios\|requests.get" src/ \| head` | src/http/client.py:1-30 |
| FE-I-004.NET-2 | Connection pool sizing (max connections per host) | L1 | M | `graphify query "connection pool max"` | `grep -rn "maxConnTotal\|pool\|maxPoolSize" src/ \| head` |  |
| FE-I-004.NET-3 | Timeout configuration (connect / read / write) | L1 | M | `graphify query "timeout connect read"` | `grep -rn "setConnectTimeout\|setReadTimeout\|timeout" src/ \| head` |  |
| FE-I-004.NET-4 | Retry policy (count / backoff / idempotency check) | L1 | M | `graphify query "retry backoff"` | `grep -rn "RetryTemplate\|@Retryable\|backoff" src/ \| head` |  |
| FE-I-004.NET-5 | TLS / certificate handling (custom CA / mTLS / pinning) | L1 | H | `graphify query "TLS certificate"` | `grep -rn "SSLContext\|TrustManager\|certificate" src/ \| head` |  |
| FE-I-004.NET-6 | Proxy configuration (HTTP/SOCKS) | L1 | M | `graphify query "proxy http socks"` | `grep -rn "Proxy-Authorization\|setProxy\|http_proxy" src/ \| head` |  |
| FE-I-004.NET-7 | Circuit breaker / fault tolerance | L1 | H | `graphify query "circuit breaker"` | `grep -rn "Resilience4j\|Hystrix\|circuit_breaker" src/ \| head` |  |
| FE-I-004.NET-8 | Request / response logging (body capture, redaction) | L1 | M | `graphify query "request logging redacted"` | `grep -rn "RequestLogger\|logRequest\|interceptor" src/ \| head` |  |
| FE-I-004.NET-9 | Streaming / chunked transfer | L1 | M | `graphify query "chunked streaming"` | `grep -rn "StreamingBody\|chunked\|streamFor" src/ \| head` |  |
| FE-I-004.NET-10 | Authentication header injection (Bearer / API key / mTLS) | L1 | M | `graphify query "authorization header"` | `grep -rn "Authorization\|Bearer\|X-API-Key" src/ \| head` | src/http/client.py:1-30 |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash

## Output Spec

`project-infra-network/SKILL.md` must:
- Real YAML frontmatter
- Sections shaped by data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`.

## Red Flags

- Reuses this template's table verbatim
- Java-specific HTTP guidance in a non-Java project
- Says "应该设置超时" without citing the actual config call
- Description starts with "远程网络访问" instead of "Use when"
