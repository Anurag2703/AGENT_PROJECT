# -------------------------------------------------------
# File: backend/app/ws_handler.py
# Purpose: WebSocket management / broadcast helpers
# -------------------------------------------------------


from fastapi import WebSocket
from typing import Dict, Set
import asyncio

# Dictionary to store connected WebSockets for each task
connections: Dict[str, Set[WebSocket]] = {}
# Lock for thread-safe operations
_conn_lock = asyncio.Lock()


async def register_ws(task_id: str, websocket: WebSocket):
    """Register a websocket connection for a specific task."""
    async with _conn_lock:
        if task_id not in connections:
            connections[task_id] = set()
        connections[task_id].add(websocket)
        print(f"[WS] Registered connection for task: {task_id}")


async def unregister_ws(task_id: str, websocket: WebSocket):
    """Unregister a websocket connection."""
    async with _conn_lock:
        if task_id in connections:
            connections[task_id].discard(websocket)
            if not connections[task_id]:
                connections.pop(task_id)
            print(f"[WS] Unregistered connection for task: {task_id}")


async def broadcast(task_id: str, message: dict):
    """Broadcast a message to all connected clients for a given task."""
    async with _conn_lock:
        active_connections = list(connections.get(task_id, set()))

    for ws in active_connections:
        try:
            await ws.send_json(message)
        except Exception as e:
            print(f"[WS] Failed to send message to {task_id}: {e}")
            try:
                await unregister_ws(task_id, ws)
            except Exception:
                pass