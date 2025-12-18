from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models.weekly_stats import WeeklyStats
from routers.auth import get_current_user

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/weekly")
def get_weekly_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return (
        db.query(WeeklyStats)
        .filter(WeeklyStats.user_id == current_user["id"])
        .order_by(WeeklyStats.week_start.desc())
        .all()
    )
