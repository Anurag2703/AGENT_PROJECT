# -------------------------------------------------------
# File: backend/app/models.py
# Purpose: Pydantic models / Task DB models
# -------------------------------------------------------


from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime

class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"

class StartTaskRequest(BaseModel):
    prompt: str
    options: Optional[Dict[str, Any]] = {}

class TaskState(BaseModel):
    task_id: str
    prompt: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    result: Optional[Dict[str, Any]] = None
    trace: Optional[List[Dict[str,Any]]] = []