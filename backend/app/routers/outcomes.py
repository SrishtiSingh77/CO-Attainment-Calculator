from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(tags=["outcomes"])


@router.get("/courses/{course_id}/outcomes", response_model=List[schemas.CourseOutcomeOut])
def list_outcomes(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.get_outcomes_for_course(db, course_id)


@router.post(
    "/courses/{course_id}/outcomes",
    response_model=schemas.CourseOutcomeOut,
    status_code=201,
)
def create_outcome(
    course_id: int, outcome: schemas.CourseOutcomeCreate, db: Session = Depends(get_db)
):
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.create_outcome(db, course_id, outcome)


@router.put("/outcomes/{co_id}", response_model=schemas.CourseOutcomeOut)
def update_outcome(
    co_id: int, outcome: schemas.CourseOutcomeUpdate, db: Session = Depends(get_db)
):
    db_outcome = crud.get_outcome(db, co_id)
    if not db_outcome:
        raise HTTPException(status_code=404, detail="Course outcome not found")
    return crud.update_outcome(db, db_outcome, outcome)


@router.delete("/outcomes/{co_id}", status_code=204)
def delete_outcome(co_id: int, db: Session = Depends(get_db)):
    db_outcome = crud.get_outcome(db, co_id)
    if not db_outcome:
        raise HTTPException(status_code=404, detail="Course outcome not found")
    crud.delete_outcome(db, db_outcome)
