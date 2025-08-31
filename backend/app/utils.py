# -------------------------------------------------------
# File: backend/app/utils.py
# Purpose: Helper util functions (IDs, logging)
# -------------------------------------------------------


import uuid
from datetime import datetime

def gen_task_id():
    return uuid.uuid4().hex

def now_iso():
    return datetime.utcnow().isoformat() + "Z"