---
name: frontend-redux
description: Use when architect-stage0 detects a React project using Redux Toolkit (@reduxjs/toolkit) for state management, including slices, thunks, and selectors - frontend framework skill
---

# Redux Frontend Skill

> Loaded by architect-stage0 when `package.json` contains `@reduxjs/toolkit` or `src/store/index.ts` exports a Redux store.
> This file is a survey questionnaire, NOT prescriptive guidance. The AI must run graphify queries and cite `path/to/file:line` for every claim.

## Investigation Points

| ID | Question | graphify query | bash fallback |
|----|----------|----------------|---------------|
| FR-1 | Which Redux version (Redux Toolkit / classic Redux / RTK Query)? | `graphify query "Redux Toolkit createSlice"` | `grep -E '"(@reduxjs/toolkit\|redux\|react-redux)"' package.json` |
| FR-2 | Slice organization (one slice per feature / domain / UI vs global)? | `graphify query "Redux slice feature"` | `grep -rn "createSlice\|Slice = " src/ \| head` |
| FR-3 | Async action handling (createAsyncThunk / RTK Query / custom middleware)? | `graphify query "createAsyncThunk RTK Query"` | `grep -rn "createAsyncThunk\|createApi\|fetchBaseQuery" src/ \| head` |
| FR-4 | Selector pattern (reselect / useSelector / memoized)? | `graphify query "Redux selector reselect"` | `grep -rn "createSelector\|useSelector" src/ \| head` |
| FR-5 | Store configuration (configureStore / combineReducers / middleware list)? | `graphify query "configureStore middleware"` | `grep -rn "configureStore\|combineReducers" src/ \| head` |
| FR-6 | React integration (Provider / hooks / connect HOC)? | `graphify query "React Redux Provider"` | `grep -rn "<Provider\|useDispatch\|useSelector" src/ \| head` |
| FR-7 | Normalization (normalizr / entityAdapter / custom)? | `graphify query "Redux entityAdapter normalizr"` | `grep -rn "createEntityAdapter\|normalizr\|normalize" src/ \| head` |
| FR-8 | DevTools integration (browser extension / redux-devtools middleware)? | `graphify query "Redux DevTools"` | `grep -rn "devTools\|composeWithDevTools" src/ \| head` |
| FR-9 | Persistence (redux-persist / localStorage / custom)? | `graphify query "Redux persist localStorage"` | `grep -rn "redux-persist\|localStorage\|persistReducer" src/ \| head` |
| FR-10 | Testing (Redux Testing Library / mock store / integration tests)? | `graphify query "Redux test mock store"` | `grep -rn "configureMockStore\|@testing-library\|renderWithProviders" src/ \| head` |

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
- Listing generic "Redux best practices" not specific to the actual project
- Citing Vue/Pinia conventions in a React project
- Description starting with "Redux 框架调查" instead of "Use when"

## Companion Files

This skill ships with Pattern B (reusable tool):

- `scripts/detect-redux.sh` — detects whether a project uses Redux Toolkit
- `scripts/extract-redux-patterns.sh` — extracts slice/thunk/selector patterns

If the data warrants Pattern C (heavy reference), add top-level `patterns.md` or `examples.md` files. Do NOT nest references in subdirectories.
