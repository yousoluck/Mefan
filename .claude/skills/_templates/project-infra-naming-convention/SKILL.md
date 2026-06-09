---
name: project-infra-naming-convention
description: Use when architect-stage0 needs to extract the project's variable, function, class, and file naming conventions from the actual source code - cross-cutting infra helper
---

# Naming Convention Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-infra-naming-convention` skill.
> Output must cite real `path/to/file:line` evidence; no template content may be copied.

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-I-000.NAME-1 | Variable naming style (camelCase / snake_case / kebab-case) | L1 | M | `graphify query "variable name camel snake"` | `grep -rE "^(let\|const\|var)\s+[a-z_]+" src/ 2>/dev/null \| head -5; grep -rE "^\s*(public\|private)\s+\w+\s+\w+" src/ 2>/dev/null \| head -5` |  |
| FE-I-000.NAME-2 | Function naming style (camelCase / snake_case) | L1 | M | `graphify query "function name style"` | `grep -rE "function\s+\w+\|def\s+\w+" src/ 2>/dev/null \| head -5` |  |
| FE-I-000.NAME-3 | Class naming (PascalCase / suffix conventions like `*Service` / `*Repository`) | L1 | M | `graphify query "class name suffix"` | `grep -rE "class\s+[A-Z]\w+" src/ 2>/dev/null \| head -5` |  |
| FE-I-000.NAME-4 | File naming (kebab-case / snake_case / camelCase) | L1 | M | `graphify query "file name style"` | `ls src/ 2>/dev/null \| head -10; ls app/ 2>/dev/null \| head -10` |  |
| FE-I-000.NAME-5 | Constant naming (UPPER_SNAKE_CASE vs lower) | L1 | M | `graphify query "constant UPPER_SNAKE"` | `grep -rE "const\s+[A-Z_]+\s*=" src/ 2>/dev/null \| head -5` |  |
| FE-I-000.NAME-6 | Boolean prefix (is/has/should/can) | L1 | M | `graphify query "boolean prefix is has"` | `grep -rE "(is\|has\|should)\w+\s*=" src/ 2>/dev/null \| head -5` |  |
| FE-I-000.NAME-7 | Test file naming (*.test.ts / test_*.py / *_spec.rb) | L1 | M | `graphify query "test file name"` | `find . -name "*test*" -o -name "*spec*" 2>/dev/null \| grep -v node_modules \| head -10` |  |
| FE-I-000.NAME-8 | Private member prefix (_underscore / __double_underscore / m_camelCase) | L1 | M | `graphify query "private member prefix"` | `grep -rE "_\w+\s*=\|self\._\w+" src/ 2>/dev/null \| head -5` |  |
| FE-I-000.NAME-9 | Module / package naming (kebab-case / snake_case) | L1 | M | `graphify query "module package name"` | `ls src/*/ -d 2>/dev/null \| head -10; find . -name "package.json" -not -path "*/node_modules/*" \| head -5` |  |
| FE-I-000.NAME-10 | Acronym handling (HttpClient vs HTTPClient vs Httpclient) | L1 | H | `graphify query "acronym HTTP URL ID"` | `grep -rE "(HTTP\|URL\|ID\|API)\w+" src/ 2>/dev/null \| head -5` |  |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash
4. Sample at least 5-10 files per category; a single example is not a convention

## Output Spec

`project-infra-naming-convention/SKILL.md` must:
- Real YAML frontmatter
- One section per category (variable, function, class, file, ...)
- Each section cites 3+ `path/to/file:line` examples of actual usage
- For conflicting styles (e.g. some files snake_case, some camelCase), report the dominant style and note exceptions
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`. "Should" is forbidden; "is" requires evidence.

## Red Flags

- Output reuses the "good vs bad" binary framing from the old `naming-variables.ts` example
- Output prescribes a single style (e.g. "all camelCase") without checking the actual codebase
- Output cites zero or only one file:line per claim
- Description starts with "命名规范" instead of "Use when"
