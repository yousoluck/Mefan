---
name: project-infra-config
description: Use when architect-stage0 needs to characterize how the project loads, validates, and hot-reloads configuration (env vars, YAML, Consul, Nacos, etcd) - tier 1 for FE-I-008
---

# Configuration Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-infra-config` skill.
> Output must cite real `path/to/file:line` evidence; no template content may be copied.

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-I-008.CFG-1 | Config source priority (env > file > defaults) | L1 | M | `graphify query "config source priority"` | `grep -rn "application.yml\|.env\|getenv" src/ \| head` | src/config/settings.py:1-40 |
| FE-I-008.CFG-2 | Type-safe binding (e.g. `@ConfigurationProperties`, `pydantic-settings`) | L1 | M | `graphify query "configuration properties bind"` | `grep -rn "@ConfigurationProperties\|BaseSettings\|pydantic" src/ \| head` |  |
| FE-I-008.CFG-3 | Hot reload / dynamic refresh (Spring Cloud Config / Nacos / etcd watch) | L1 | H | `graphify query "hot reload refresh"` | `grep -rn "@RefreshScope\|@NacosValue\|watch.*config" src/ \| head` |  |
| FE-I-008.CFG-4 | Environment isolation (dev / staging / prod profiles) | L1 | M | `graphify query "profile environment dev prod"` | `find . -name "application-*.yml" -o -name "*.env.*" \| head` | config/settings/dev.py:1-30 |
| FE-I-008.CFG-5 | Secret interpolation (e.g. `${VAULT_SECRET}`) | L1 | M | `graphify query "secret interpolation vault"` | `grep -rn "vault\|VAULT_\|@Value.*\\\\${" src/ \| head` |  |
| FE-I-008.CFG-6 | Config validation on startup | L1 | M | `graphify query "config validation startup"` | `grep -rn "@Validated\|@PostConstruct.*config\|validate.*config" src/ \| head` |  |
| FE-I-008.CFG-7 | Default value fallback policy | L1 | M | `graphify query "default value fallback"` | `grep -rn "getProperty.*default\|: default" src/ \| head` |  |
| FE-I-008.CFG-8 | Config change audit / change tracking | L1 | H | `graphify query "config change audit"` | `grep -rn "configChange\|audit.*config\|change_history" src/ \| head` |  |
| FE-I-008.CFG-9 | Feature flag integration (LaunchDarkly / Unleash / custom) | L1 | M | `graphify query "feature flag toggle"` | `grep -rn "FeatureFlag\|Unleash\|launchdarkly\|@Toggle" src/ \| head` |  |
| FE-I-008.CFG-10 | Config encryption at rest | L1 | H | `graphify query "config encryption KMS"` | `grep -rn "encrypt.*config\|jasypt\|EncryptedProperty" src/ \| head` | src/config/settings.py:1-40 |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash

## Output Spec

`project-infra-config/SKILL.md` must:
- Real YAML frontmatter
- Sections shaped by data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`.

## Red Flags

- Reuses this template's table verbatim
- Spring `@ConfigurationProperties` guidance for a non-Spring project
- Says "应该使用 @ConfigurationProperties" without citing the actual class
- Description starts with "配置管理" instead of "Use when"
