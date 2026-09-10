# Rubrix.ai — CO Attainment Calculator

A web app for faculty to define Course Outcomes, record student scores against them, and get server-calculated attainment percentages per outcome.

**Live Demo:** https://co-attainment-calculator.vercel.app/
**API Documentation:** https://co-attainment-calculator.onrender.com/docs

## Overview

Outcome-Based Education (OBE) requires institutions to track how well students meet defined learning outcomes for each course. This app is a small, focused implementation of that workflow for a faculty member:

1. Create a **Course**
2. Define its **Course Outcomes (COs)** — the specific skills students should demonstrate
3. Add **Students** to the course
4. Enter each student's **Score** against each CO
5. View **Attainment %** per CO — the share of students who met a given threshold

Everything after step 4 is computed server-side from the same recorded scores, so changing the threshold in step 5 recalculates attainment instantly without re-entering any data.

## CO Attainment Logic

```
Attainment % = (students with score >= threshold / students with a recorded score) × 100
```

- A score **exactly equal to** the threshold counts as attained (`>=`, not `>`).
- Students with **no recorded score** for a CO are excluded from the denominator — they are not treated as having failed to meet it.
- The threshold itself is validated server-side to be between 0 and 100 (`FastAPI Query(..., ge=0, le=100)`); score entry is validated to the same 0–100 range in the UI.
- The calculation always runs server-side, in [`app/services/attainment.py`](backend/app/services/attainment.py) — a plain Python function with no FastAPI or SQLAlchemy dependency, so it's independently unit tested.

**Example:** a CO has 5 recorded scores: `45, 50, 62, 78, 90`. At a threshold of `50`, four scores (`50, 62, 78, 90`) meet it → **80% attainment**.

## Features

**Course Management**
- Create, list, update, and delete courses

**Course Outcome Management**
- Add, list, update, and delete COs for a course

**Student Management**
- Add, list, update, and delete students within a course

**Score Management**
- Editable student × CO score grid, loaded in a single API call
- Save-on-blur entry with inline 0–100 validation
- Duplicate-score prevention and student/CO course-consistency checks on the backend

**Attainment Calculation**
- Adjustable threshold input, recalculated live via the backend endpoint
- No attainment math performed in the frontend

**Developer / API**
- Auto-generated interactive API docs (Swagger UI) at `/docs`
- Idempotent seed script for repeatable local setup

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, SQLite, Pydantic, Pytest
**Frontend:** React, Vite, JavaScript, Tailwind CSS, Axios
**Deployment:** Vercel (frontend), Render (backend)

## Architecture

```
React frontend
      ↓
   REST API
      ↓
   FastAPI
      ↓
CRUD / Services
      ↓
 SQLAlchemy
      ↓
   SQLite
```

The attainment calculation is intentionally isolated from both the API and the database layer — `services/attainment.py` takes plain numbers in and returns plain numbers out. Routers fetch data via `crud.py` and pass raw scores into the service; the service has no knowledge of HTTP or the database.

## Project Structure

```
backend/
  app/
    main.py            FastAPI app setup, CORS, router registration
    database.py         SQLAlchemy engine/session
    models.py            Course, CourseOutcome, Student, Score
    schemas.py            Pydantic request/response models
    crud.py                Database access functions
    services/
      attainment.py         Independent attainment calculation
    routers/
      courses.py, outcomes.py, students.py, scores.py, attainment.py
    seed.py                 Idempotent seed data script
  tests/
    test_attainment_service.py

frontend/
  src/
    api/client.js          Centralized Axios API client
    components/             CourseList, OutcomeForm, StudentForm, ScoreGrid, AttainmentResults
    pages/                   CoursesPage, CourseDetailPage
```

## Demo

The screenshots below aren't included in this repository — see the live app instead: https://co-attainment-calculator.vercel.app/

## Local Setup

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
```

Runs at `http://127.0.0.1:8000`, docs at `http://127.0.0.1:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://127.0.0.1:5173`. Set `VITE_API_URL` in the frontend environment to point at a non-local backend; it falls back to `http://127.0.0.1:8000` when unset.

## Database / Seed Data

SQLite, stored at `backend/rubrix.db` (gitignored). Tables are created automatically on app startup via `Base.metadata.create_all()`.

`python -m app.seed` loads:

- **3 courses** — Database Systems (4 COs, 8 students), Operating Systems (5 COs, 7 students), Software Engineering (3 COs, 6 students)
- A score for every student × CO combination in each course (85 scores total), with marks randomized between 35 and 98

The script checks for existing course codes before inserting, so re-running it does not create duplicates.

## API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/courses` | List courses |
| GET | `/courses/{course_id}` | Get a course |
| POST | `/courses` | Create a course |
| PUT | `/courses/{course_id}` | Update a course |
| DELETE | `/courses/{course_id}` | Delete a course |
| GET | `/courses/{course_id}/outcomes` | List COs for a course |
| POST | `/courses/{course_id}/outcomes` | Create a CO |
| PUT | `/outcomes/{co_id}` | Update a CO |
| DELETE | `/outcomes/{co_id}` | Delete a CO |
| GET | `/courses/{course_id}/students` | List students in a course |
| POST | `/courses/{course_id}/students` | Add a student |
| PUT | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |
| GET | `/courses/{course_id}/scores` | Score grid — students, outcomes, and scores in one call |
| POST | `/scores` | Record a score |
| PUT | `/scores/{score_id}` | Update a score |
| DELETE | `/scores/{score_id}` | Delete a score |
| GET | `/outcomes/{co_id}/attainment?threshold=X` | Attainment % for a CO at a given threshold |

## Testing

```bash
cd backend
pytest -v
```

Tests cover `calculate_attainment` in isolation: a score exactly at the threshold, above it, below it, an empty score list (no division-by-zero), a mixed-scores case, and invalid threshold values. The boundary test — **a score exactly equal to the threshold counts as attained** — is the one the assignment calls out explicitly, and it's asserted directly rather than inferred from a larger scenario.

No API-level integration tests are included; CRUD and endpoint behavior were verified manually during development.

## Design Decisions

1. **Independent attainment service** — `calculate_attainment()` has no FastAPI or SQLAlchemy dependency, so it's testable with plain Python and reusable outside the API if needed.
2. **Server-side calculation only** — the frontend never computes attainment; it displays whatever the backend returns, keeping the business rule in one place.
3. **Centralized frontend API client** — all HTTP calls live in `api/client.js`, so components call named functions (`getCourses()`, `createScore()`) instead of constructing requests inline.
4. **Single-call score grid** — `GET /courses/{id}/scores` returns students, outcomes, and scores together, so the frontend builds the full grid without a request per cell.
5. **Validation and error handling** — the backend rejects duplicate scores for the same student/CO and scores referencing a student and CO from different courses; the frontend validates score entries against the 0–100 range inline before saving.

## Deployment

- **Frontend:** Vercel — https://co-attainment-calculator.vercel.app/
- **Backend:** Render — https://co-attainment-calculator.onrender.com
- **Database:** SQLite

SQLite on Render's free tier is a deliberate scope tradeoff for this assignment rather than a production setup: the filesystem isn't guaranteed to persist across redeploys or restarts, so data can reset. For a production deployment, PostgreSQL (e.g. Render's managed Postgres) would replace SQLite without any change to the application logic, since access goes through SQLAlchemy.

## What Was Not Implemented

Scoped out to keep the core workflow complete and reliable within the assignment's time budget:

- JWT authentication / faculty-scoped courses
- Docker Compose
- Pagination on list endpoints

## Future Improvements

- JWT-based faculty authentication and course ownership
- PostgreSQL for production persistence
- API-level integration tests
- CSV import/export for scores
- Bulk score entry
- Basic reporting/visualizations for attainment trends

## Author

**Srishti Singh**

Built as a Software Engineering Intern screening assignment for Rubrix.ai.