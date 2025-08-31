# -------------------------------------------------------
# File: backend/AGENT.md
# Purpose: Documentation about the agent & API
# -------------------------------------------------------


# AGENT.md — Graph-Structured AI Agent

## Purpose
This backend implements a graph-structured AI agent for:
- Task planning
- Retrieval
- Computation (local or delegated)
- Self-critique loops
- Streaming intermediate outputs to frontends through WebSocket for smooth UX

## Architecture
- Backend (FastAPI) orchestrates tasks using `langgraph_runner.py`.
- `langgraph_runner` implements nodes: plan -> retrieve -> compute -> self-critique -> finalize.
- WebSocket endpoint `/ws/run/{task_id}` streams intermediate events to connected clients.
- REST endpoints:
  - POST `/api/start` — start a new task (returns `task_id`)
  - GET `/api/status/{task_id}` — query saved state
  - POST `/api/cancel/{task_id}` — (demo) cancel
- `a2a_client.py` is a stub for delegating tasks to remote A2A agents.

## LangGraph integration
Replace the placeholder runner with an actual LangGraph workflow:
- Create LangGraph nodes for each step and register a callback to send partial outputs.
- Ensure each node can call `stream_callback(task_id, message)` to broadcast progress.
- Persist node outputs into the `TaskState.trace`.

## A2A integration
- `a2a_client.py` should implement:
  - Agent discovery via Agent Cards
  - HTTP/JSON-RPC or SSE communication
  - Auth and timeouts
- Use A2A for specialized compute/retrieval agents; the runner demonstrates delegation points.

## Streaming contract (WebSocket messages)
Each message is a JSON object with keys like:
- `phase`: one of ["start","plan","retrieve","compute","critique","final","completed","error"]
- `message`: human text
- `time`: ISO timestamp
- optional additional fields: `chunk_index`, `items`, `trace_item`, etc.

Example:
```json
{"phase":"compute","message":"analysis part 1","chunk_index":0,"time":"2025-08-30T12:00:00Z"}