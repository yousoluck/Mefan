---
name: project-ui-generic
description: Use when architect-stage0 needs to characterize a UI component, page, or interaction pattern, but no specific project-ui-{name}/ template matches - tier 2 for L4-UI
---

# Generic UI Skill — Investigation Template

> Architect-stage0 uses this template to generate a `project-ui-{name}/` skill when:
> - The feature has a UI surface (component / page / form / interaction)
> - BUT no specific template exists for that UI element
> - AND the AI must improvise based on graphify queries alone

The generated skill name will be `project-ui-{name}` (replace `{name}` with the actual UI element detected in `feature-elements.md`).

## Investigation Points

| ID | Investigation Point | L | Difficulty | graphify query | bash fallback | Code Target |
|----|---------------------|---|------------|----------------|---------------|-------------|
| FE-U-UI-1 | Framework (React / Vue / Svelte / Angular / vanilla) | L4 | M | `graphify query "React Vue Svelte component"` | `grep -rn "from 'react'\|from 'vue'\|@Component" src/ \| head` |  |
| FE-U-UI-2 | Component file convention (*.tsx / *.vue / *.svelte) | L4 | M | `graphify query "component file extension"` | `find . -name "*.tsx" -o -name "*.vue" -o -name "*.svelte" 2>/dev/null \| head` |  |
| FE-U-UI-3 | State management (Redux / Pinia / Zustand / context / useState) | L4 | M | `graphify query "state management"` | `grep -rn "useState\|createSlice\|defineStore" src/ \| head` |  |
| FE-U-UI-4 | Routing pattern (file-based / config / declarative) | L4 | M | `graphify query "routing file-based"` | `grep -rn "createBrowserRouter\|vue-router\|<Route" src/ \| head` |  |
| FE-U-UI-5 | Form handling (Formik / react-hook-form / native) | L4 | M | `graphify query "form handling library"` | `grep -rn "useForm\|Formik\|v-model" src/ \| head` |  |
| FE-U-UI-6 | Styling approach (CSS modules / Tailwind / styled-components / SCSS) | L4 | M | `graphify query "styling CSS Tailwind"` | `grep -rn "className=\|@apply\|styled\\." src/ \| head` |  |
| FE-U-UI-7 | Data fetching (SWR / React Query / fetch / axios) | L4 | M | `graphify query "data fetching SWR"` | `grep -rn "useSWR\|useQuery\|axios\\.\\|fetch(" src/ \| head` |  |
| FE-U-UI-8 | Accessibility (ARIA roles, keyboard nav, focus mgmt) | L4 | H | `graphify query "accessibility ARIA keyboard"` | `grep -rn "aria-\|role=\|onKeyDown" src/ \| head` |  |
| FE-U-UI-9 | Internationalization (i18n library / locale handling) | L4 | M | `graphify query "internationalization i18n"` | `grep -rn "useTranslation\|i18next\|t(" src/ \| head` |  |
| FE-U-UI-10 | Error boundary / loading state conventions | L4 | M | `graphify query "error boundary loading"` | `grep -rn "ErrorBoundary\|isLoading\|Suspense" src/ \| head` |  |
## Query Execution Rules

1. Tokens from graph.json or `.vocab.txt` only
2. Max 12 tokens per query
3. On failure, retry once with synonym, then bash

## Output Spec

`project-ui-{name}/SKILL.md` must:
- Real YAML frontmatter
- Replace `{name}` with the actual UI element
- Sections shaped by data, not by this 10-point table
- Every fact cited with `path/to/file:line`
- Missing data → `[需人工补充]`

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`. No framework prescriptions without project evidence.

## Red Flags

- Output reuses the 10-point table verbatim
- Output cites React `useState` in a Vue project
- Description starts with "UI 组件" instead of "Use when"
- The `name:` field still contains the literal placeholder `{name}`
