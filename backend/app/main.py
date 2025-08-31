# -------------------------------------------------------
# File: backend/app/main.py
# Purpose: FastAPI backend with Gemini streaming
# -------------------------------------------------------



from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from .routes_rest import router as rest_router
from .storage import get_task
from .db import create_db_and_tables
from .config import settings
from .gemini_client import GeminiClient

# Initialize FastAPI
app = FastAPI(title="Graph-Agent (FastAPI + LangGraph Streaming)")

# Include REST routes
app.include_router(rest_router, prefix="/api")

# CORS settings
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate Gemini Client
gemini = GeminiClient()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.websocket("/ws/run/{task_id}")
async def ws_run(websocket: WebSocket, task_id: str):
    """
    WebSocket endpoint for streaming Gemini responses.
    """
    await websocket.accept()
    print(f"[WS] Client connected for Task ID: {task_id}")

    try:
        # Retrieve task prompt from DB
        task = await get_task(task_id)
        if not task or not task.get("prompt"):
            await websocket.send_text("Error: Prompt not found for this task ID.")
            await websocket.close()
            return

        prompt = task["prompt"]
        print(f"[WS] Streaming started for prompt: {prompt}")

        # Stream Gemini response
        async for chunk in gemini.stream_generate(prompt):
            await websocket.send_text(chunk)
            await asyncio.sleep(0.02)  # smooth streaming effect

        # Notify frontend of completion
        await websocket.send_text("[DONE]")
        print(f"[WS] Streaming completed for Task ID: {task_id}")

    except WebSocketDisconnect:
        print(f"[WS] Disconnected: {task_id}")
    except Exception as e:
        print(f"[WS] Error: {e}")
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()
        print(f"[WS] Closed connection for Task ID: {task_id}")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
