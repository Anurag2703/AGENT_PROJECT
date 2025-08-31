# Backend — Graph Agent

## Quick start (dev)
1. python -m venv .venv
2. .venv/Scripts/Activate.ps1
3. pip install -r requirements.txt
4. uvicorn app.main:app --reload

## API
- POST /api/start { prompt: "..." } -> returns TaskState with task_id
- WS /ws/run/{task_id} -> stream messages

## Notes
- Replace LangGraph runner with real LangGraph workflow if using the official package.


## Install:
    pip install 'uvicorn[standard]'