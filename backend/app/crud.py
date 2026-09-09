"""
CRUD functions. Routers call these instead of touching the DB session
directly, keeping route handlers thin.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app import models, schemas


# ---------- Course ----------

def get_courses(db: Session) -> List[models.Course]:
    return db.query(models.Course).all()


def get_course(db: Session, course_id: int) -> Optional[models.Course]:
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def create_course(db: Session, course: schemas.CourseCreate) -> models.Course:
    db_course = models.Course(code=course.code, name=course.name)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(
    db: Session, db_course: models.Course, course: schemas.CourseUpdate
) -> models.Course:
    db_course.code = course.code
    db_course.name = course.name
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, db_course: models.Course) -> None:
    db.delete(db_course)
    db.commit()


# ---------- CourseOutcome ----------

def get_outcomes_for_course(db: Session, course_id: int) -> List[models.CourseOutcome]:
    return (
        db.query(models.CourseOutcome)
        .filter(models.CourseOutcome.course_id == course_id)
        .all()
    )


def get_outcome(db: Session, co_id: int) -> Optional[models.CourseOutcome]:
    return (
        db.query(models.CourseOutcome)
        .filter(models.CourseOutcome.id == co_id)
        .first()
    )


def create_outcome(
    db: Session, course_id: int, outcome: schemas.CourseOutcomeCreate
) -> models.CourseOutcome:
    db_outcome = models.CourseOutcome(
        course_id=course_id, code=outcome.code, description=outcome.description
    )
    db.add(db_outcome)
    db.commit()
    db.refresh(db_outcome)
    return db_outcome


def update_outcome(
    db: Session,
    db_outcome: models.CourseOutcome,
    outcome: schemas.CourseOutcomeUpdate,
) -> models.CourseOutcome:
    db_outcome.code = outcome.code
    db_outcome.description = outcome.description
    db.commit()
    db.refresh(db_outcome)
    return db_outcome


def delete_outcome(db: Session, db_outcome: models.CourseOutcome) -> None:
    db.delete(db_outcome)
    db.commit()


# ---------- Student ----------

def get_students_for_course(db: Session, course_id: int) -> List[models.Student]:
    return (
        db.query(models.Student).filter(models.Student.course_id == course_id).all()
    )


def get_student(db: Session, student_id: int) -> Optional[models.Student]:
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def create_student(
    db: Session, course_id: int, student: schemas.StudentCreate
) -> models.Student:
    db_student = models.Student(
        course_id=course_id, name=student.name, roll_number=student.roll_number
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(
    db: Session, db_student: models.Student, student: schemas.StudentUpdate
) -> models.Student:
    db_student.name = student.name
    db_student.roll_number = student.roll_number
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, db_student: models.Student) -> None:
    db.delete(db_student)
    db.commit()


# ---------- Score ----------

def get_scores_for_course(db: Session, course_id: int) -> List[models.Score]:
    return (
        db.query(models.Score)
        .join(models.Student, models.Score.student_id == models.Student.id)
        .filter(models.Student.course_id == course_id)
        .all()
    )


def get_scores_for_outcome(db: Session, co_id: int) -> List[models.Score]:
    return db.query(models.Score).filter(models.Score.co_id == co_id).all()


def get_score(db: Session, score_id: int) -> Optional[models.Score]:
    return db.query(models.Score).filter(models.Score.id == score_id).first()


def get_score_by_student_and_co(
    db: Session, student_id: int, co_id: int
) -> Optional[models.Score]:
    return (
        db.query(models.Score)
        .filter(models.Score.student_id == student_id, models.Score.co_id == co_id)
        .first()
    )


def create_score(db: Session, score: schemas.ScoreCreate) -> models.Score:
    db_score = models.Score(
        student_id=score.student_id, co_id=score.co_id, marks=score.marks
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def update_score(
    db: Session, db_score: models.Score, score: schemas.ScoreUpdate
) -> models.Score:
    db_score.marks = score.marks
    db.commit()
    db.refresh(db_score)
    return db_score


def delete_score(db: Session, db_score: models.Score) -> None:
    db.delete(db_score)
    db.commit()
