# -------------------------------------------------------
# File: backend/app/langgraph_runner.py
# Purpose: LangGraph orchestration + streaming hooks
# -------------------------------------------------------


import asyncio
from typing import Callable, Dict, Any, List
from .utils import now_iso
from .a2a_client import A2AClient
from .gemini_client import GeminiClient
from .storage import update_task, get_task

class LangGraphRunner:
    def __init__(self, a2a_client: A2AClient = None, gemini_client: GeminiClient = None):
        self.a2a = a2a_client or A2AClient()
        self.gemini = gemini_client or GeminiClient()

    async def run(self, task_id: str, prompt: str, stream_callback: Callable[[str, Dict[str,Any]], None], options: Dict[str,Any] = None):
        options = options or {}
        try:
            await stream_callback(task_id, {"phase":"start", "time": now_iso(), "message":"Task started."})
            # Plan
            plan = f"Plan: analyze and create subtasks for prompt (len={len(prompt)})"
            await stream_callback(task_id, {"phase":"plan", "message":plan, "time": now_iso()})
            await update_task(task_id, append_trace={"phase":"plan","message":plan,"time":now_iso()})

            # Retrieve (stubbed) - could call an internal vector DB or A2A retrieval agent
            retrieve_msg = "Retrieving context / docs..."
            await stream_callback(task_id, {"phase":"retrieve", "message":retrieve_msg, "time": now_iso()})
            await update_task(task_id, append_trace={"phase":"retrieve","message":retrieve_msg,"time":now_iso()})
            # simulate retrieval result
            retrieved = ["doc1 snippet about API", "doc2 snippet about orchestration"]
            await asyncio.sleep(0.1)

            # Compute: use Gemini for generation; stream chunks to UI
            compute_msg = "Computing with Gemini..."
            await stream_callback(task_id, {"phase":"compute", "message": compute_msg})
            await update_task(task_id, append_trace={"phase":"compute","message":compute_msg,"time":now_iso()})

            # If options ask to delegate to A2A:
            if options.get("delegate_compute"):
                await stream_callback(task_id, {"phase":"compute", "message":"Delegating compute to A2A agent..."})
                a2a_res = await self.a2a.delegate_task(options.get("delegate_url"), {"task": prompt})
                await update_task(task_id, append_trace={"phase":"compute_delegate", "result":a2a_res, "time": now_iso()})
                await stream_callback(task_id, {"phase":"compute", "message": f"A2A result: {str(a2a_res)[:200]}"})
            else:
                # stream from GeminiClient
                async for idx, chunk in aenumerate(self.gemini.stream_generate(prompt, chunk_size=120)):
                    await stream_callback(task_id, {"phase":"compute", "chunk_index": idx, "message": chunk, "time": now_iso()})
                    await update_task(task_id, append_trace={"phase":"compute_chunk","index":idx,"chunk":chunk,"time":now_iso()})

            # Self-critique
            critique = "Self-critique: check for missing references and hallucinations."
            await stream_callback(task_id, {"phase":"critique", "message": critique})
            await update_task(task_id, append_trace={"phase":"critique","message":critique,"time":now_iso()})
            await asyncio.sleep(0.1)

            # Finalize: produce final answer (gather last compute traces)
            final_result = f"Final concise answer derived from prompt: {prompt[:200]}"
            await stream_callback(task_id, {"phase":"final", "message": final_result})
            await update_task(task_id, result={"final": final_result}, status="completed")
            await stream_callback(task_id, {"phase":"completed", "message": "Task completed."})
            return {"status":"ok", "final":final_result}

        except Exception as e:
            await update_task(task_id, status="failed", result={"error": str(e)})
            await stream_callback(task_id, {"phase":"error", "message": str(e)})
            return {"status":"error", "error": str(e)}


# helper aenumerate for async generator enumeration
async def aenumerate(agen):
    i = 0
    async for item in agen:
        yield i, item
        i += 1