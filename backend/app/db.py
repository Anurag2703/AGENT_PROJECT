# -------------------------------------------------------
# File: backend/app/db.py
# Purpose: SQLAlchemy setup
# -------------------------------------------------------

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
import json
from .config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class TaskORM(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    prompt = Column(Text)
    status = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    result = Column(Text, nullable=True)   # JSON dump
    trace = Column(Text, nullable=True)    # JSON dump

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "prompt": self.prompt,
            "status": self.status,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
            "result": json.loads(self.result) if self.result else None,
            "trace": json.loads(self.trace) if self.trace else [],
        }

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)