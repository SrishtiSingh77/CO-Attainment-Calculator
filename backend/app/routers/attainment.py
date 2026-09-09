from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.services.attainment import calculate_attainment

router = APIRouter(tags=["attainment"])


@router.get("/outcomes/{co_id}/attainment", response_model=schemas.AttainmentOut)
def get_attainment(
    co_id: int,
    threshold: float = Query(..., ge=0, le=100),
    db: Session = Depends(get_db),
):
    outcome = crud.get_outcome(db, co_id)
    if not outcome:
        raise HTTPException(status_code=404, detail="Course outcome not found")

    scores = crud.get_scores_for_outcome(db, co_id)
    marks = [s.marks for s in scores]  # only students with a recorded score

    result = calculate_attainment(scores=marks, threshold=threshold)

    return schemas.AttainmentOut(
        co_id=co_id,
        threshold=threshold,
        total_students=result["total_students"],
        students_met=result["students_met"],
        attainment_percentage=result["attainment_percentage"],
    )
