# AI Software Engineering Agent

An autonomous coding pipeline built on LangGraph: a requirement goes in,
working code + tests + review + security scan + performance notes + docs +
deployment artifacts come out. Three feedback loops (failing tests, a
rejected review, or a flagged security issue) route back to the Coder
automatically, up to `MAX_ITER` times.

```
Planner → Coder → Tester ─(fail)→ Coder
                    │(pass)
                    ▼
                 Reviewer ─(reject)→ Coder
                    │(approve)
                    ▼
                 Security ─(vulnerable)→ Coder
                    │(secure)
                    ▼
              Performance → Documentation → Deployment → done
```

## Structure
```
agents/
  planner.py        requirement -> plan
  coder.py           plan (+ feedback) -> source files
  tester.py          files -> test files, runs real pytest in a subprocess
  reviewer.py        files+tests+results -> review, approve/reject
  security.py        static regex scan + LLM review -> secure/vulnerable
  performance.py      files + test runtime -> optimization notes
  documentation.py    files -> README.md + docs/API.md
  deployment.py       files -> Dockerfile, docker-compose.yml, CI workflow
utils/workspace.py    file-block parsing, disk writes, pytest runner, static scan
state.py               shared graph state
llm.py                 OpenRouter client wrapper
graph.py               LangGraph wiring + loop/gate logic
main.py                CLI entry point
api.py                 FastAPI: POST /run, GET /runs/{id}, GET /runs/{id}/download
static/index.html      single-file dashboard (no build step) served by the API
```

Every run gets its own `workspaces/<run_id>/` directory containing the
actual generated project — source, tests, docs, and deployment files —
which is what tests actually execute against and what the download link
zips up.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
export $(cat .env | xargs)
```
Get a key at https://openrouter.ai/keys. `OPENROUTER_MODEL` accepts any
OpenRouter slug (`openai/gpt-4o-mini`, `google/gemini-2.0-flash-001`, etc.)
— swap providers without touching code.

## Run — CLI
```bash
python main.py "Create a REST API for a todo list with JWT auth"
```

## Run — API + dashboard
```bash
uvicorn api:app --reload
# open http://localhost:8000
```
or with Docker:
```bash
docker compose up --build
```

## What's real vs. simplified
This is an MVP of the full spec, not the whole enterprise platform. What's
actually implemented and working:
- All 8 agents run for real against an LLM via OpenRouter, in a real
  LangGraph state machine with three genuine conditional feedback loops.
- Tests actually execute (`pytest` in a subprocess against the generated
  files), not just an LLM guessing pass/fail.
- Security agent combines a real static regex scan with an LLM review.
- A working FastAPI backend + a minimal dashboard, not just a CLI.

What's deliberately left out or simplified, versus the original spec:
- No Postgres/Redis/Alembic — generated projects can ask for them, but this
  platform itself has no database; run state lives in memory (`RUNS` dict)
  and resets on restart.
- No React/Vite/Tailwind dashboard — one static HTML+JS file instead, no
  build step, polling instead of a live-updating graph view.
- No Prometheus/Grafana/tracing — none of the observability stack.
- No Kubernetes manifests or AWS deployment — the Deployment agent
  generates Docker/Compose/CI *for the generated project*, not for this
  platform, and doesn't go as far as K8s.
- Performance agent is LLM analysis + test-suite wall time, not real
  profiling (no cProfile/memory_profiler wired in).

Extending any of these is mechanical: add `agents/x.py` with an
`x_node(state)` function, wire it into `graph.py`, and — if it should gate
the loop — add a conditional edge like the existing ones.
