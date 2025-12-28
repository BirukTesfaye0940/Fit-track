from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from routers.auth import get_current_user
from mcp.weekly_signals import get_weekly_signals
from ai.gemini_client import weekly_coach_feedback

router = APIRouter(prefix="/ai/coach", tags=["AI Coach"])


@router.get("/weekly")
def weekly_ai_coach(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    signals = get_weekly_signals(db, current_user["id"])

    if not signals.get("worked_out"):
        return {
            "summary": "No workouts logged this week.",
            "coach_message": "Log at least one workout so I can help you improve."
        }

    coach_text = weekly_coach_feedback(signals)

    return {
        "summary": signals,
        "coach_message": coach_text
    }
