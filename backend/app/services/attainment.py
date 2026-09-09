"""
Attainment calculation — the core business logic of this app.

Deliberately framework-agnostic: no FastAPI, no SQLAlchemy, no DB
session. It takes plain numbers in and returns plain numbers out, so
it can be unit tested in isolation and reused anywhere.
"""

from typing import Sequence


def calculate_attainment(scores: Sequence[float], threshold: float) -> dict:
    """
    Calculate the % of students who met or exceeded a threshold for one CO.

    Args:
        scores: raw marks for every student who has a score for this CO.
                 Students with no score for this CO must be excluded by
                 the caller before this function is invoked.
        threshold: the mark a student must reach to count as "met".
                    Must be between 0 and 100 inclusive.

    Returns:
        {
            "total_students": int,   # students with a score for this CO
            "students_met": int,     # students whose score >= threshold
            "attainment_percentage": float,
        }

    Rules:
        - score >= threshold counts as met (score == threshold counts).
        - No scores at all -> 0% attainment, no division by zero.
    """
    if not 0 <= threshold <= 100:
        raise ValueError("threshold must be between 0 and 100")

    total_students = len(scores)

    if total_students == 0:
        return {
            "total_students": 0,
            "students_met": 0,
            "attainment_percentage": 0.0,
        }

    students_met = sum(1 for score in scores if score >= threshold)
    attainment_percentage = (students_met / total_students) * 100

    return {
        "total_students": total_students,
        "students_met": students_met,
        "attainment_percentage": round(attainment_percentage, 2),
    }
