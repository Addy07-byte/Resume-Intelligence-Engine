# Resume Intelligence Engine — v2 Agentic RAG Roadmap

## Why v2

v1 was a linear RAG pipeline (parse → chunk → embed → retrieve → generate) deployed on Streamlit. It worked as a proof of concept but has three production gaps: no evals, no observability, no agentic reasoning. v2 addresses all three.

## Target architecture

Single ReAct-style agent with tool-calling. The agent orchestrates retrieval, self-reflection, and generation. Tools: retrieve_resume_chunks, retrieve_jd_requirements, compare_qualifications, generate_match_report, grade_my_answer.

Backend: FastAPI on Railway. Frontend: Next.js (Streamlit retired). Observability: LangSmith traces on every request. Evals: 20-case test set run on every deploy.

## Phases

### Phase 1 — Foundation (Days 1-2)
- [ ] Refactor Streamlit to FastAPI backend with Pydantic request/response models
- [ ] Deploy FastAPI on Railway (free tier)
- [ ] Add structured logging with request_id, per-stage latency, token counts
- [ ] Wire Streamlit as a thin frontend calling the API
- Acceptance: curl the deployed API, get a valid response with logged trace

### Phase 2 — Evals Harness (Days 3-4)
- [ ] Build 20 (resume, JD) test cases in /evals/cases as JSON
- [ ] Define 3 metrics: retrieval_accuracy, grounding_rate, end_to_end_success
- [ ] Implement eval runner in /evals/run_evals.py
- [ ] Record v1 baseline numbers in /evals/results_v1.md
- [ ] Integrate LangSmith tracing, tag runs by version
- Acceptance: `python evals/run_evals.py` prints baseline metrics

### Phase 3 — Agentic Upgrade (Days 5-7)
- [ ] Replace linear LangGraph with ReAct agent using LangGraph prebuilt
- [ ] Define 5 tools in /tools/ directory
- [ ] Add self-reflection: grade output against source, retry retrieval if grounding is weak
- [ ] Add query rewriting: reformulate JD requirement before retrieving
- [ ] Add multi-hop retrieval for compound requirements
- [ ] Re-run evals, record v2 numbers in /evals/results_v2.md
- Acceptance: v2 beats v1 on at least 2 of 3 metrics

### Phase 4 — Production Hardening (Days 8-9)
- [ ] Add Redis caching for embeddings
- [ ] Add exponential backoff retry on LLM calls
- [ ] Add rate limiting on FastAPI endpoint
- [ ] Add cost tracking: log tokens per request, compute $/query
- [ ] Build simple /metrics dashboard page: p50 latency, p95 latency, error rate, $/query
- Acceptance: dashboard renders with real traffic data from LangSmith

### Phase 5 — Resume Update (Day 10)
- [ ] Update RIE project bullets on resume with real metrics
- [ ] Update README with architecture diagram, eval results table, API docs
- [ ] Write 1 blog post on what I learned, publish on Medium
- [ ] Update LinkedIn Featured section with blog link + repo link
- Acceptance: blog post is live, resume bullets now contain numbers

## Guardrails for me

- 3-hour build block per day. Not 6. Not 10. Three.
- 2 applications per morning continue. Building does not pause the job search.
- Sunday is fully off.
- If stuck for more than 30 minutes on any task, paste the error to Claude and ask for help. Don't grind.
- If I catch myself adding "one more feature" outside the phase scope, write it in /BACKLOG.md and move on.
- Each phase ends with a commit and a push. Visible progress on GitHub.

## What this unlocks for my resume

Before v2: "Built a multi-step RAG pipeline using LangChain, LangGraph, ChromaDB, and GPT-4o, with source citations."

After v2: "Agentic RAG system with ReAct tool-calling, self-reflection, query rewriting, and multi-hop retrieval. Deployed FastAPI backend on Railway with LangSmith observability, Redis embedding cache, and cost tracking. 20-case eval harness showing retrieval accuracy [X%], grounding rate [Y%], end-to-end task success [Z%]. p95 latency [N]s, $/query [$M]."

The second version lands interviews. The first version doesn't.