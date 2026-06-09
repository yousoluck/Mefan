---
name: frontend-vue
description: Use when architect-stage0 detects a Vue project (Vue 2 or Vue 3, with or without Pinia / Vuex / Vue Router) for component composition and reactivity - frontend framework skill
---

# Vue Frontend Skill

> Loaded by architect-stage0 when `package.json` contains `vue` or `src/store/` uses Pinia / Vuex.
> This file is a survey questionnaire, NOT prescriptive guidance. The AI must run graphify queries and cite `path/to/file:line` for every claim.

## Investigation Points

| ID | Question | graphify query | bash fallback |
|----|----------|----------------|---------------|
| FV-1 | Which Vue version (Vue 2 Options API vs Vue 3 Composition API)? | `graphify query "Vue 2 3 version composition"` | `grep -E '"vue":' package.json; grep -rE "Vue.extend\|defineComponent\|<script setup" src/ \| head` |
| FV-2 | State management (Pinia / Vuex 4 / Vuex 3 / provide-inject)? | `graphify query "Pinia Vuex store"` | `grep -rn "defineStore\|createStore\|useStore" src/ \| head` |
| FV-3 | Router setup (Vue Router 4 / Vue Router 3 / hash vs history mode)? | `graphify query "Vue Router 4 createRouter"` | `grep -rn "createRouter\|createWebHistory\|createWebHashHistory" src/ \| head` |
| FV-4 | Component composition (SFC *.vue / JSX / render functions)? | `graphify query "Vue SFC .vue component"` | `find src/ -name "*.vue" \| head; find src/ -name "*.tsx" -o -name "*.jsx" \| head` |
| FV-5 | Reactivity primitives (ref / reactive / computed / watch vs Vue 2 data)? | `graphify query "Vue ref reactive watch"` | `grep -rn "ref(\|reactive(\|computed(\|watch(" src/ \| head` |
| FV-6 | Lifecycle hooks (onMounted / onUnmounted / created)? | `graphify query "Vue lifecycle onMounted"` | `grep -rn "onMounted\|onUnmounted\|mounted()\|created()" src/ \| head` |
| FV-7 | Form handling (vee-validate / vuelidate / native v-model)? | `graphify query "Vue form validation v-model"` | `grep -rn "vee-validate\|vuelidate\|v-model" src/ package.json` |
| FV-8 | Build tooling (Vite / Vue CLI / Nuxt / webpack)? | `graphify query "Vite Vue CLI Nuxt"` | `grep -E '"(@vitejs/plugin-vue\|@vue/cli-service\|nuxt\|vite)"' package.json; ls vite.config.* nuxt.config.* 2>/dev/null` |
| FV-9 | Testing (Vitest / Jest / @vue/test-utils / Cypress)? | `graphify query "Vue test vitest"` | `grep -rn "vitest\|@vue/test-utils\|cypress" package.json; find . -name "*.spec.ts" -o -name "*.test.ts" \| head` |
| FV-10 | TypeScript usage (vue-tsc / <script setup lang="ts">)? | `graphify query "Vue TypeScript script setup"` | `grep -rn "lang=\"ts\"\|<script setup\|vue-tsc" src/ package.json \| head` |

## Output Requirements

When architect-stage0 fills this in:

1. Real YAML frontmatter (`---` block, `name` + `description: Use when ...`)
2. Sections shaped by the actual data — do NOT mirror the 10-question table above
3. Every claim cited with `path/to/file:line`
4. Missing data → `[需人工补充]`, never silent fabrication

## Iron Law

**NO SKILL WITHOUT EVIDENCE** — Each claim requires `path/to/file:line`.

## Red Flags

- Reusing the 10-question table verbatim as the output structure
- Listing generic "Vue best practices" not specific to the actual project
- Citing React conventions in a Vue project
- Description starting with "Vue 框架调查" instead of "Use when"

## Companion Files (none)

This skill is Pattern A (self-contained). Add `scripts/` only if a detection helper is required.
