# -------------------------------------------------------
# File: backend/app/config.py
# Purpose: Configuration, env var reading
# -------------------------------------------------------

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

class Settings(BaseSettings):
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    WS_PATH: str = os.getenv("WS_PATH", "/ws/run")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DEV_AUTH_BYPASS: bool = os.getenv("DEV_AUTH_BYPASS", "True").lower() == "true"

settings = Settings()