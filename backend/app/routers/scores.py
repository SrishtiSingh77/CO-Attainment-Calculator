from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(tags=["scores"])


@router.get("/courses/{course_id}/scores", response_model=schemas.ScoreGridOut)
def get_score_grid(course_id: int, db: Session = Depends(get_db)):
    """
    Returns students, outcomes, and scores for a course in one call so
    the frontend can build the full student x CO grid without a
    request per cell.
    """
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return schemas.ScoreGridOut(
        students=crud.get_students_for_course(db, course_id),
        outcomes=crud.get_outcomes_for_course(db, course_id),
        scores=crud.get_scores_for_course(db, course_id),
    )


@router.post("/scores", response_model=schemas.ScoreOut, status_code=201)
def create_score(score: schemas.ScoreCreate, db: Session = Depends(get_db)):
    student = crud.get_student(db, score.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    outcome = crud.get_outcome(db, score.co_id)
    if not outcome:
        raise HTTPException(status_code=404, detail="Course outcome not found")

    if student.course_id != outcome.course_id:
        raise HTTPException(
            status_code=400,
            detail="Student and course outcome must belong to the same course",
        )

    existing = crud.get_score_by_student_and_co(db, score.student_id, score.co_id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="A score already exists for this student and CO. Use PUT to update it.",
        )

    return crud.create_score(db, score)


@router.put("/scores/{score_id}", response_model=schemas.ScoreOut)
def update_score(score_id: int, score: schemas.ScoreUpdate, db: Session = Depends(get_db)):
    db_score = crud.get_score(db, score_id)
    if not db_score:
        raise HTTPException(status_code=404, detail="Score not found")
    return crud.update_score(db, db_score, score)


@router.delete("/scores/{score_id}", status_code=204)
def delete_score(score_id: int, db: Session = Depends(get_db)):
    db_score = crud.get_score(db, score_id)
    if not db_score:
        raise HTTPException(status_code=404, detail="Score not found")
    crud.delete_score(db, db_score)
