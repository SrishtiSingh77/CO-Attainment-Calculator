from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(tags=["students"])


@router.get("/courses/{course_id}/students", response_model=List[schemas.StudentOut])
def list_students(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.get_students_for_course(db, course_id)


@router.post(
    "/courses/{course_id}/students", response_model=schemas.StudentOut, status_code=201
)
def create_student(
    course_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)
):
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.create_student(db, course_id, student)


@router.put("/students/{student_id}", response_model=schemas.StudentOut)
def update_student(
    student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)
):
    db_student = crud.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return crud.update_student(db, db_student, student)


@router.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    crud.delete_student(db, db_student)
