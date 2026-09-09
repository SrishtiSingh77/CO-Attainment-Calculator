"""
Database configuration.

Uses SQLite for simplicity, as allowed by the assignment.
`check_same_thread=False` is required because FastAPI can access the
same SQLite connection from different threads within a single request
lifecycle; SQLite otherwise refuses cross-thread use by default.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./rubrix.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
