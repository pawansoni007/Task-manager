# AI Usage

This project was built with AI assistance. Below is an honest account of how it was used.

### 1. Which AI tools did you use?
Claude Code (Anthropic) as a pair-programming assistant in the terminal.

### 2. What did you ask AI to help with?
- Turning the assignment brief into a concrete plan and a clean layered architecture.
- Scaffolding the FastAPI backend (domain model, repository pattern, service, routers, schemas).
- Scaffolding the React + TypeScript frontend (API client, `useTasks` hook, components, styling).
- Writing the pytest suite and a browser-driven end-to-end check.
- Producing the deployment config (Render/Vercel) and this documentation.

### 3. Which parts of the code were AI-assisted?
Effectively all of the initial scaffolding was AI-generated from my requirements: the backend layers,
the frontend components, the tests, and the deploy/docs files. I directed the design decisions —
the React + FastAPI stack, the repository pattern with a swappable SQL backend, and the explicit
`app/api/routers/` package separation were my calls, and I had the AI restructure when the first cut
didn't match what I wanted.

### 4. What did you manually change or verify?
- I reviewed the overall structure and asked for a dedicated router package mounted in `main.py`,
  rather than flat route files.
- I confirmed the layering rule holds: routers do HTTP only, the service owns business logic, and
  repositories are thin storage boundaries.
- I checked the API design (status codes, camelCase contract, validation behavior) against the brief.

### 5. How did you test the solution?
- **Unit/contract tests:** `pytest` — 26 tests covering service logic (validation, filter, search,
  stats, lifecycle) and the API (happy paths plus `404`/`422`). All green.
- **SQL path:** verified the SQLAlchemy repository persists and reloads across instances with SQLite.
- **End-to-end:** ran the real frontend against the real backend in a headless browser and walked the
  full flow — empty state, validation, create (with priority/due date), complete, filter, search,
  edit, delete, and counts — confirming each step (see the screenshot in the README).

### 6. Did AI produce anything incorrect or risky?
- A test initially asserted `createdAt == updatedAt`, but two separate timestamp factory calls
  differed by microseconds. I fixed the domain model so a new task shares a single timestamp.
- The first dependency-injection helper tried to `lru_cache` a Pydantic settings object (not
  hashable); I replaced it with a simple lazy singleton.
- During end-to-end testing, cross-origin requests were blocked until `CORS_ORIGINS` was set
  correctly — a good reminder that the deployed frontend origin must be configured on the backend.

### 7. What would you improve if you had more time?
- Ship with a Postgres instance wired into the deploy by default for out-of-the-box persistence.
- Add optimistic UI updates and frontend component/e2e tests in CI.
- Add sorting and pagination for larger task lists.
