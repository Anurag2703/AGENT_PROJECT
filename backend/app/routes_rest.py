# -------------------------------------------------------
# File: backend/app/routes_rest.py
# Purpose: REST endpoints (start task, status, cancel)
# -------------------------------------------------------


from fastapi import APIRouter, BackgroundTasks, HTTPException
from .models import StartTaskRequest, TaskState, TaskStatus
from .utils import gen_task_id, now_iso
from .storage import save_task, update_task, get_task
from .langgraph_runner import LangGraphRunner
from .ws_handler import broadcast
from datetime import datetime
import asyncio

router = APIRouter()
_runner = LangGraphRunner()

async def _stream_cb(task_id: str, msg: dict):
    # persist and broadcast
    # append to trace via storage.update_task
    await update_task(task_id, append_trace=msg)
    await broadcast(task_id, msg)

@router.post("/start", response_model=TaskState)
async def start_task(req: StartTaskRequest):
    task_id = gen_task_id()
    tdict = {
        "task_id": task_id,
        "prompt": req.prompt,
        "status": TaskStatus.pending.value,
        "result": None,
        "trace": []
    }
    # save to DB
    saved = await save_task(tdict)
    # background execution
    async def run_and_finalize():
        await update_task(task_id, status=TaskStatus.running.value)
        res = await _runner.run(task_id, req.prompt, stream_callback=_stream_cb, options=req.options or {})
        if res.get("status") == "ok":
            await update_task(task_id, status=TaskStatus.completed.value, result={"final": res.get("final")})
        else:
            await update_task(task_id, status=TaskStatus.failed.value, result={"error": res.get("error")})
    asyncio.create_task(run_and_finalize())
    # return TaskState (read back)
    t = await get_task(task_id)
    # convert to TaskState pydantic
    from .models import TaskState as TS
    return TS(**t)

@router.get("/status/{task_id}", response_model=TaskState)
async def status(task_id: str):
    t = await get_task(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    from .models import TaskState as TS
    return TS(**t)

@router.post("/cancel/{task_id}")
async def cancel(task_id: str):
    t = await get_task(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    await update_task(task_id, status=TaskStatus.cancelled.value)
    await broadcast(task_id, {"phase":"cancelled","message":"Task cancelled by user"})
    return {"status":"cancelled"}