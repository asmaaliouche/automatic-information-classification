"""
Database connection and session management.
Uses SQLAlchemy to connect to a local PostgreSQL database.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL — defaults to local PostgreSQL, but supports SQLite for easier POC deployment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./data/attrition.db" # Default switched to SQLite for easier development and deployment
)

# Connect arguments needed for SQLite (multi-threading)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides a database session and ensures it is closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
