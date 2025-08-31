# -------------------------------------------------------
# File: backend/app/storage.py
# Purpose: Simple in-memory or file-based persistence
# -------------------------------------------------------


from .db import SessionLocal, TaskORM, create_db_and_tables
from .models import TaskState, TaskStatus
from datetime import datetime
import json
from sqlalchemy.exc import NoResultFound
from fastapi.concurrency import run_in_threadpool

create_db_and_tables()

def _orm_to_taskstate(orm: TaskORM) -> TaskState:
    return TaskState(
        task_id=orm.task_id,
        prompt=orm.prompt,
        status=TaskStatus(orm.status),
        created_at=orm.created_at,
        updated_at=orm.updated_at,
        result=json.loads(orm.result) if orm.result else None,
        trace=json.loads(orm.trace) if orm.trace else []
    )

def save_task_sync(task_dict):
    session = SessionLocal()
    orm = TaskORM(
        task_id=task_dict["task_id"],
        prompt=task_dict["prompt"],
        status=task_dict["status"],
        result=json.dumps(task_dict.get("result")) if task_dict.get("result") else None,
        trace=json.dumps(task_dict.get("trace", []))
    )
    session.add(orm)
    session.commit()
    session.refresh(orm)
    session.close()
    return orm.to_dict()

async def save_task(task_dict):
    return await run_in_threadpool(save_task_sync, task_dict)

async def get_task(task_id: str):
    def _get():
        session = SessionLocal()
        q = session.query(TaskORM).filter(TaskORM.task_id == task_id)
        orm = q.one_or_none()
        session.close()
        return orm.to_dict() if orm else None
    return await run_in_threadpool(_get)

async def update_task(task_id: str, **updates):
    def _update():
        session = SessionLocal()
        orm = session.query(TaskORM).filter(TaskORM.task_id == task_id).one_or_none()
        if not orm:
            session.close()
            return None
        if "status" in updates:
            orm.status = updates["status"]
        if "result" in updates:
            orm.result = json.dumps(updates["result"])
        if "trace" in updates:
            orm.trace = json.dumps(updates["trace"])
        if "append_trace" in updates:
            existing = json.loads(orm.trace) if orm.trace else []
            existing.append(updates["append_trace"])
            orm.trace = json.dumps(existing)
        session.add(orm)
        session.commit()
        out = orm.to_dict()
        session.close()
        return out
    return await run_in_threadpool(_update)