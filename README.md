# Rubrix.ai — CO Attainment Calculator

Reference Code: <RX-CODE>

A small web app for a faculty member to define Course Outcomes (COs)
for a course, enter each student's score against each CO, and see the
calculated attainment % per CO.

## OBE / Attainment, in short

- **Course Outcome (CO):** a specific skill a student should
  demonstrate after a course (e.g. "Write a normalized database
  schema").
- **Attainment:** the % of students who scored at or above a target
  threshold for that CO.

  ```
  attainment % = (students with score >= threshold) / (students with a recorded score) * 100
  ```

  A score exactly equal to the threshold counts as met. Students with
  no recorded score for a CO are excluded from the denominator
  entirely — they're not counted as "not met".

## Features

- CRUD for courses, course outcomes, students, and scores
- An editable student × CO score grid, loaded in one API call
- Per-CO attainment results with an adjustable threshold, calculated
  entirely server-side
- Seed data so the app isn't empty on first run
- A pure, independently-tested attainment calculation function

## Tech Stack

**Backend:** Python 3.10+, FastAPI, SQLAlchemy, SQLite, Pydantic, Pytest
**Frontend:** React, Vite, JavaScript, Tailwind CSS, Axios

## Project Structure

```
backend/
  app/
    main.py          FastAPI app, CORS, router registration
    database.py       engine, session, Base
    models.py          SQLAlchemy models
    schemas.py         Pydantic request/response models
    crud.py             DB access functions
    services/
      attainment.py     pure attainment calculation (no FastAPI/SQLAlchemy)
    routers/
      courses.py, outcomes.py, students.py, scores.py, attainment.py
    seed.py             idempotent seed script
  tests/
    test_attainment_service.py

frontend/
  src/
    api/client.js        centralized API calls (axios)
    components/           CourseList, OutcomeForm, StudentForm, ScoreGrid, AttainmentResults
    pages/                 CoursesPage, CourseDetailPage
    App.jsx
```

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m app.seed          # populate sample data (safe to re-run)
uvicorn app.main:app --reload
```

API runs at `http://127.0.0.1:8000`. Interactive docs at
`http://127.0.0.1:8000/docs`.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://127.0.0.1:5173`. Requires the backend running on
port 8000 (CORS is already configured for the Vite dev server).

## Database / Seed

SQLite, file-based (`backend/rubrix.db`, gitignored). Tables are
created automatically on app startup via
`Base.metadata.create_all()`. Run `python -m app.seed` to load 3
courses, 4–5 COs each, and 6–8 students each with sample scores. The
seed script checks for existing course codes before inserting, so
re-running it won't create duplicates.

## Testing

```bash
cd backend
pytest -v
```

Covers the attainment calculation in isolation: score exactly at
threshold, above threshold, below threshold, empty score list (no
division-by-zero), a mixed-scores case, and invalid threshold values.

## API Documentation

FastAPI's auto-generated docs at `/docs` (Swagger UI) once the
backend is running.

## What's Implemented

- Full CRUD for Course, CourseOutcome, Student, Score
- `GET /courses/{id}/scores` returns students + outcomes + scores in
  one call so the frontend builds the full grid without a
  request-per-cell
- `GET /outcomes/{id}/attainment?threshold=X` — attainment endpoint
  backed by the independent calculation service
- Duplicate-score prevention (409) and student/CO-same-course
  validation (400) on score creation
- Frontend: course list, CO/student management, editable score grid
  with save-on-blur, attainment results with adjustable threshold —
  all calculation done server-side, none duplicated in the frontend
- Loading, error, and empty states throughout the UI

## What Was Not Implemented

- JWT authentication (left as optional, per assignment scope)
- Docker Compose (left as optional, per assignment scope)
- No pagination on lists — fine at seed-data scale, would matter at
  real scale
- No optimistic UI rollback on failed score save (it shows an error
  border but doesn't revert the input value)
- No API-level tests (FastAPI `TestClient`) — only the attainment
  service is unit tested per the assignment's explicit ask; CRUD
  paths were verified manually via curl during development instead

## What I'd Add With More Time

- JWT auth with courses scoped to the faculty member who created them
- API-level tests with an in-memory test DB fixture
- PATCH-style partial updates instead of full-replace PUT
- CSV import/export for scores
- Docker Compose for one-command local setup
