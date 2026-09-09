"""
SQLAlchemy models.

Relationships:
    Course 1--N CourseOutcome   (cascade delete)
    Course 1--N Student         (cascade delete)
    CourseOutcome 1--N Score    (cascade delete)
    Student 1--N Score          (cascade delete)

A Score always ties a Student to a CourseOutcome, and both of those
belong to the same Course. That cross-consistency (a score can't
reference a student from one course and a CO from another) is enforced
in the CRUD layer rather than the schema, to keep the schema simple.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False, unique=True, index=True)  # e.g. "CS301"
    name = Column(String, nullable=False)  # e.g. "Database Systems"

    outcomes = relationship(
        "CourseOutcome", back_populates="course", cascade="all, delete-orphan"
    )
    students = relationship(
        "Student", back_populates="course", cascade="all, delete-orphan"
    )


class CourseOutcome(Base):
    __tablename__ = "course_outcomes"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    code = Column(String, nullable=False)  # e.g. "CO1"
    description = Column(String, nullable=False)

    course = relationship("Course", back_populates="outcomes")
    scores = relationship(
        "Score", back_populates="course_outcome", cascade="all, delete-orphan"
    )


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    name = Column(String, nullable=False)
    roll_number = Column(String, nullable=False)

    course = relationship("Course", back_populates="students")
    scores = relationship(
        "Score", back_populates="student", cascade="all, delete-orphan"
    )


class Score(Base):
    __tablename__ = "scores"
    __table_args__ = (
        # A student can only have one score per CO. Re-submitting is an
        # update (upsert), not a new row.
        UniqueConstraint("student_id", "co_id", name="uq_student_co"),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    co_id = Column(Integer, ForeignKey("course_outcomes.id"), nullable=False)
    marks = Column(Float, nullable=False)  # raw marks obtained, e.g. out of 100

    student = relationship("Student", back_populates="scores")
    course_outcome = relationship("CourseOutcome", back_populates="scores")
