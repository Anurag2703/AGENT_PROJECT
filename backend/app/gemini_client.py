# -------------------------------------------------------
# File: backend/app/gemini_client.py
# Purpose: Streaming wrapper for Gemini API
# -------------------------------------------------------


import os
import google.generativeai as genai
from .config import settings

class GeminiClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def generate(self, prompt: str, max_tokens: int = 512) -> str:
        """
        Non-streaming version — returns full text at once
        """
        response = self.model.generate_content(
            prompt, generation_config={"max_output_tokens": max_tokens}
        )
        return response.text

    async def stream_generate(self, prompt: str):
        """
        Streaming generator yielding each chunk of text.
        """
        stream = self.model.generate_content(prompt, stream=True)
        for chunk in stream:
            if chunk.text:
                yield chunk.text