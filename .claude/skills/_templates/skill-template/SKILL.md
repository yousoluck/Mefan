---
name: skill-template
description: Use when architect-stage0 needs to determine which template to use for generating a new project skill, or when no other template matches the feature element under analysis - tier-3 fallback
---

# Skill Template (Skeleton)

> This is NOT a real skill. It is the meta-template used by architect-stage0 when:
> - No `project-{type}-{exact-name}/` template exists (tier 1 miss)
> - No `project-{type}-generic/` template exists (tier 2 miss)
> - Architect must construct a skill from raw graphify queries alone (tier 3 fallback)

## Template Selection Three-Tier Fallback

| Tier | Path | When Used |
|------|------|-----------|
| 1 | `.claude/skills/_templates/project-{type}-{exact-name}/` | Exact feature-element name match |
| 2 | `.claude/skills/_templates/project-{type}-generic/` | Type-only match (api/domain/service/ui/feature/infra) |
| 3 | This file (skill-template) | No match — AI improvises from graphify queries |

## When This Tier-3 Fallback Applies

Architect-stage0 falls through to this template when:
- The feature element under analysis has no specific template
- AND no generic template covers its `type`
- Example: a project using an unusual technology stack with no `project-infra-{name}` template

## Output Requirements (for AI generating from this template)

When architect-stage0 falls through to this template, the AI MUST:

1. Load the standard: invoke `Skill(skill="superpowers:writing-skills")`
2. Design 5-10 investigation points based on the feature element name
3. For each investigation point, write one `graphify query` and one `bash fallback`
4. Execute the queries, collect real evidence (`file:line` references)
5. Write SKILL.md with:
   - Real YAML frontmatter (`name` + `description` "Use when...")
   - Sections determined by the data, NOT by this template
   - Every fact cited with `path/to/file:line` evidence
   - Missing-data sections marked `[需人工补充]`, never silent fabrication

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — A skill section without a `file:line` citation is fabrication. The Iron Law applies at three levels:
- No template section copied verbatim into the output
- No "应该怎样" or "should" phrasing substituted for actual project data
- No code from `_templates/.trash/` (historical hardcoded Spring Boot / Redux snippets) reused

## Red Flags

- Generating a skill that looks like a tutorial or template fill-in
- Including code samples without `path/to/file:line` evidence
- Using "应该怎样" or "should" phrasing in the output
- Frontmatter description that starts with "包含..." or lists contents
- No investigation-points table in the AI's working notes before writing

## Companion Files (none)

This template produces Pattern A (self-contained) skills by default. The AI may promote to Pattern B (with `scripts/`) or Pattern C (with companion `*.md` files at top level) only when the data warrants it.
