# -------------------------------------------------------
# File: backend/app/config.py
# Purpose: Configuration, env var reading
# -------------------------------------------------------


from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    WS_PATH: str = "/ws/run"
    DATABASE_URL: str = "sqlite:///./tasks.db"
    GEMINI_API_KEY: str = "AIzaSyCuu16jQLiPDpbUVaZQu9x5NF2N5nVDZ_M"  # put in .env for real usage
    DEV_AUTH_BYPASS: bool = True

settings = Settings()