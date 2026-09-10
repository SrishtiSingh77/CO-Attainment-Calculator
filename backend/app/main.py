import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models  # noqa: F401  (ensures models are registered on Base)
from app.routers import courses, outcomes, students, scores, attainment

# Create tables on startup. Fine for SQLite + a scoped assignment;
# a real project would use Alembic migrations instead.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rubrix.ai CO Attainment Calculator")

# Allow local dev origins always, plus the deployed frontend URL when
# FRONTEND_URL is set (e.g. the Vercel deployment talking to Render).
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok"}


app.include_router(courses.router)
app.include_router(outcomes.router)
app.include_router(students.router)
app.include_router(scores.router)
app.include_router(attainment.router)