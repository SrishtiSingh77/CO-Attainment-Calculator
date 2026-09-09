"""
Seed script. Safe to re-run: it checks for existing courses by `code`
before inserting, so it won't create duplicates.

Run with:  python -m app.seed
"""

import random

from app.database import Base, engine, SessionLocal
from app import models

Base.metadata.create_all(bind=engine)

COURSES = [
    {
        "code": "CS301",
        "name": "Database Systems",
        "outcomes": [
            ("CO1", "Design a normalized relational database schema"),
            ("CO2", "Write complex SQL queries involving joins and aggregation"),
            ("CO3", "Explain transaction management and ACID properties"),
            ("CO4", "Apply indexing strategies to optimize query performance"),
        ],
        "students": [
            "Aarav Sharma", "Diya Patel", "Ishaan Verma", "Kavya Reddy",
            "Rohan Gupta", "Ananya Iyer", "Vivaan Nair", "Sara Khan",
        ],
    },
    {
        "code": "CS302",
        "name": "Operating Systems",
        "outcomes": [
            ("CO1", "Explain process scheduling algorithms"),
            ("CO2", "Implement synchronization using semaphores and locks"),
            ("CO3", "Describe memory management and paging techniques"),
            ("CO4", "Analyze deadlock detection and avoidance strategies"),
            ("CO5", "Compare file system implementations"),
        ],
        "students": [
            "Arjun Mehta", "Priya Singh", "Kabir Joshi", "Meera Rao",
            "Aditya Kumar", "Neha Desai", "Yash Malhotra",
        ],
    },
    {
        "code": "CS303",
        "name": "Software Engineering",
        "outcomes": [
            ("CO1", "Apply Agile methodology to a software project"),
            ("CO2", "Write unit and integration tests for a module"),
            ("CO3", "Design a system using appropriate architectural patterns"),
        ],
        "students": [
            "Tanvi Kulkarni", "Dev Chandra", "Riya Bansal", "Karan Malhotra",
            "Pooja Agarwal", "Siddharth Rao",
        ],
    },
]


def seed():
    db = SessionLocal()
    try:
        for course_data in COURSES:
            existing = (
                db.query(models.Course)
                .filter(models.Course.code == course_data["code"])
                .first()
            )
            if existing:
                print(f"Skipping {course_data['code']} — already seeded.")
                continue

            course = models.Course(code=course_data["code"], name=course_data["name"])
            db.add(course)
            db.flush()  # get course.id without a full commit

            outcomes = []
            for co_code, description in course_data["outcomes"]:
                outcome = models.CourseOutcome(
                    course_id=course.id, code=co_code, description=description
                )
                db.add(outcome)
                outcomes.append(outcome)
            db.flush()

            students = []
            for i, name in enumerate(course_data["students"], start=1):
                student = models.Student(
                    course_id=course.id,
                    name=name,
                    roll_number=f"{course_data['code']}-{i:03d}",
                )
                db.add(student)
                students.append(student)
            db.flush()

            # Realistic-ish marks out of 100, with some spread so
            # attainment % varies meaningfully by CO and threshold.
            for student in students:
                for outcome in outcomes:
                    marks = round(random.uniform(35, 98), 1)
                    db.add(
                        models.Score(
                            student_id=student.id, co_id=outcome.id, marks=marks
                        )
                    )

            db.commit()
            print(f"Seeded {course_data['code']} — {course_data['name']}")
    finally:
        db.close()


if __name__ == "__main__":
    random.seed(42)  # reproducible seed data across runs
    seed()
