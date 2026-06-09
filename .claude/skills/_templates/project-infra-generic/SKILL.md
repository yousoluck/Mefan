---
name: project-infra-generic
description: Use when architect-stage0 detects a project infrastructure concern (cache, db, fs, network, mq, security, logging, config) but no specific project-infra-{name}/ template matches the technology - tier 2 for L1
---

# Generic L1 Infrastructure Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-infra-{name}` skill when:
> - The infrastructure concern is identified (e.g. user is using an exotic cache backend)
> - BUT no specific template exists for that technology (e.g. no `project-infra-hazelcast/`)
> - AND the AI must improvise based on graphify queries alone

This is the L1-fallback (mirrors `project-api-generic`, `project-domain-generic`, etc. at the infra level).

## Investigation Points (Universal L1 Coverage)

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-I-GEN-1 | What is this infrastructure technology (name + version)? | L1 | M | `graphify query "infrastructure technology name"` | `grep -rn "import.*from\|require.*from" src/ \| head` |  |
| FE-I-GEN-2 | How is it initialized at app startup? | L1 | M | `graphify query "infrastructure initialization startup"` | `grep -rn "@Bean\|@PostConstruct\|main()" src/ \| head` |  |
| FE-I-GEN-3 | What configuration knobs exist? | L1 | M | `graphify query "configuration properties"` | `grep -rn "ConfigProperties\|settings\|config\." src/ \| head` |  |
| FE-I-GEN-4 | How does the rest of the app access it (DI / singleton / global)? | L1 | M | `graphify query "dependency injection singleton"` | `grep -rn "Autowired\|Inject\|singleton\|globalThis" src/ \| head` |  |
| FE-I-GEN-5 | What are the error / failure modes (timeout, connection refused, etc.)? | L1 | H | `graphify query "error timeout connection refused"` | `grep -rn "catch.*Timeout\|try.*catch\|.catch" src/ \| head` |  |
| FE-I-GEN-6 | Is there a graceful shutdown / cleanup hook? | L1 | M | `graphify query "shutdown cleanup close"` | `grep -rn "@PreDestroy\|onClose\|finally" src/ \| head` |  |
| FE-I-GEN-7 | Are there test doubles / mocks for it? | L1 | M | `graphify query "test mock stub fake"` | `find . -name "*test*" -not -path "*/node_modules/*" \| head` |  |
| FE-I-GEN-8 | How is it observed / monitored (metrics, health checks)? | L1 | M | `graphify query "health check metric monitor"` | `grep -rn "HealthIndicator\|@Observed\|/health" src/ \| head` |  |
| FE-I-GEN-9 | How does it interact with other infra components (db, cache, mq)? | L1 | H | `graphify query "interact with database cache"` | `grep -rn "import.*Repository\|import.*Cache\|@Autowired.*Service" src/ \| head` |  |
| FE-I-GEN-10 | Are there known anti-patterns in current usage? | L1 | H | `graphify query "anti-pattern smell"` | `grep -rn "// TODO\|// FIXME\|// HACK\|// XXX" src/ \| head` |  |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash
4. The first investigation point is critical — identify the technology before everything else

## Output Spec

`project-infra-{name}/SKILL.md` must:
- Real YAML frontmatter
- Replace `{name}` with the actual technology detected (e.g. `project-infra-hazelcast/`)
- Sections shaped by data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`. No prescriptive guidance without a citation.

## Red Flags

- Output reuses the 10-point table verbatim
- Output lists generic "best practices" not specific to this project
- Description starts with "基础设施" instead of "Use when"
- The `name:` field still contains the literal placeholder `{name}`
