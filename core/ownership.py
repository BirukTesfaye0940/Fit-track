from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.workout import Workout

def get_owned_workout(
    workout_id: int,
    user_id: int,
    db: Session
) -> Workout:
    workout = db.query(Workout).filter(Workout.id == workout_id).first()

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )

    if workout.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this workout"
        )

    return workout
