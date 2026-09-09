"""
Pydantic schemas used as FastAPI request/response bodies.

Naming convention:
    *Create -> input body for POST
    *Update -> input body for PUT (all fields required; this is a full
               replace, not a partial patch, which keeps things simple)
    *Out    -> response body
"""

from typing import List

from pydantic import BaseModel, ConfigDict


# ---------- Course ----------

class CourseCreate(BaseModel):
    code: str
    name: str


class CourseUpdate(BaseModel):
    code: str
    name: str


class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str


# ---------- CourseOutcome ----------

class CourseOutcomeCreate(BaseModel):
    code: str
    description: str


class CourseOutcomeUpdate(BaseModel):
    code: str
    description: str


class CourseOutcomeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    code: str
    description: str


# ---------- Student ----------

class StudentCreate(BaseModel):
    name: str
    roll_number: str


class StudentUpdate(BaseModel):
    name: str
    roll_number: str


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    name: str
    roll_number: str


# ---------- Score ----------

class ScoreCreate(BaseModel):
    student_id: int
    co_id: int
    marks: float


class ScoreUpdate(BaseModel):
    marks: float


class ScoreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    co_id: int
    marks: float


# ---------- Score grid (for GET /courses/{course_id}/scores) ----------
# Bundles students, COs, and scores together so the frontend can build
# the full student x CO grid without one request per cell.

class ScoreGridOut(BaseModel):
    students: List[StudentOut]
    outcomes: List[CourseOutcomeOut]
    scores: List[ScoreOut]


# ---------- Attainment ----------

class AttainmentOut(BaseModel):
    co_id: int
    threshold: float
    total_students: int
    students_met: int
    attainment_percentage: float
