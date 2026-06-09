---
name: project-infra-logging
description: Use when architect-stage0 needs to characterize the project's logging framework, log levels, structured logging, and observability hooks - tier 1 for FE-I-007
---

# Logging Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-infra-logging` skill.
> Output must cite real `path/to/file:line` evidence; no template content may be copied.

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-I-007.LOG-1 | Logging framework (Logback / Log4j2 / SLF4J / winston / pino / structlog) | L1 | M | `graphify query "logback slf4j winston"` | `grep -rn "LoggerFactory\|logback.xml\|createLogger" src/ \| head` |  |
| FE-I-007.LOG-2 | Log level policy (dev / staging / prod defaults) | L1 | M | `graphify query "log level configuration"` | `find . -name "logback*.xml" -o -name "log4j*.xml" -o -name "logger.ts" 2>/dev/null \| head` |  |
| FE-I-007.LOG-3 | Structured logging format (JSON / key-value) | L1 | M | `graphify query "structured JSON log"` | `grep -rn "logstash\|LogstashEncoder\|JSONFormatter" src/ \| head` |  |
| FE-I-007.LOG-4 | MDC / context propagation (traceId / userId) | L1 | M | `graphify query "MDC traceId context"` | `grep -rn "MDC.put\|withContext\|traceId" src/ \| head` |  |
| FE-I-007.LOG-5 | Sensitive field redaction (passwords, tokens) | L1 | M | `graphify query "redact sensitive log"` | `grep -rn "redact\|mask\|@Sensitive" src/ \| head` |  |
| FE-I-007.LOG-6 | Sampling rate for high-volume logs | L1 | M | `graphify query "log sampling rate"` | `grep -rn "sampler\|sample_rate\|Sampling" src/ \| head` |  |
| FE-I-007.LOG-7 | Correlation / request ID propagation | L1 | M | `graphify query "correlation request id"` | `grep -rn "RequestId\|X-Request-ID\|correlation" src/ \| head` |  |
| FE-I-007.LOG-8 | Distributed tracing integration (OpenTelemetry / Jaeger) | L1 | H | `graphify query "tracing opentelemetry"` | `grep -rn "OpenTelemetry\|@Observed\|@WithSpan" src/ \| head` |  |
| FE-I-007.LOG-9 | Error / exception logging policy (stack trace depth) | L1 | M | `graphify query "error exception log"` | `grep -rn "logger.error\|log.exception\|stack_trace" src/ \| head` |  |
| FE-I-007.LOG-10 | Log routing (file / stdout / syslog / cloud) | L1 | M | `graphify query "log appender stdout"` | `grep -rn "ConsoleAppender\|stdout\|syslog" src/ \| head` |  |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash

## Output Spec

`project-infra-logging/SKILL.md` must:
- Real YAML frontmatter
- Sections shaped by data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`.

## Red Flags

- Reuses this template's table verbatim
- Logback guidance for a Node.js project
- Says "应该使用 JSON 格式" without citing the actual encoder
- Description starts with "日志与调试" instead of "Use when"
