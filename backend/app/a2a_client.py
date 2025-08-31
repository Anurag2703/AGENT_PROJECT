# -------------------------------------------------------
# File: backend/app/a2a_client.py
# Purpose: A2A client stub (delegate tasks to other agents)
# -------------------------------------------------------


import asyncio
import httpx
from typing import Dict, Any

class A2AClient:
    """
    Basic A2A JSON-RPC-style delegator stub.
    - discover agent (Agent Card) and call its endpoint
    - handle timeouts and response parsing
    """

    async def delegate_task(self, agent_url: str, payload: Dict[str, Any], timeout: int = 20) -> Dict[str,Any]:
        # agent_url expected to be HTTP endpoint that accepts JSON body like {"jsonrpc":"2.0","method":"run","params":{...},"id":1}
        body = {"jsonrpc":"2.0", "method":"run", "params": payload, "id": 1}
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                r = await client.post(agent_url, json=body)
                r.raise_for_status()
                data = r.json()
                # interpret result per your A2A target agent contract
                return {"ok": True, "response": data}
            except Exception as e:
                return {"ok": False, "error": str(e)}