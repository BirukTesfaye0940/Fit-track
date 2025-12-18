from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models.weekly_stats import WeeklyStats
from routers.auth import get_current_user
from core.exceptions import FitTrackException

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/weekly")
def get_weekly_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if (db.query(WeeklyStats).filter(WeeklyStats.user_id == current_user["id"]).count() == 0):
        raise FitTrackException("No completed sets this week!!")
    return (
        db.query(WeeklyStats)
        .filter(WeeklyStats.user_id == current_user["id"])
        .order_by(WeeklyStats.week_start.desc())
        .all()
    )
