from datetime import date, timedelta
from sqlalchemy.orm import Session

from db.session import SessionLocal
from models.workout import Workout
from models.weekly_stats import WeeklyStats

def calculate_weekly_volume(user_id: int):
    db: Session = SessionLocal()

    try:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())

        workouts = (
            db.query(Workout)
            .filter(
                Workout.user_id == user_id,
                Workout.date >= week_start
            )
            .all()
        )

        total_volume = 0
        total_sets = 0
        total_reps = 0

        for workout in workouts:
            for s in workout.sets:
                total_volume += s.reps * s.weight
                total_sets += 1
                total_reps += s.reps

        stats = (
            db.query(WeeklyStats)
            .filter(
                WeeklyStats.user_id == user_id,
                WeeklyStats.week_start == week_start
            )
            .first()
        )

        if not stats:
            stats = WeeklyStats(
                user_id=user_id,
                week_start=week_start
            )
            db.add(stats)

        stats.total_volume = total_volume
        stats.total_sets = total_sets
        stats.total_reps = total_reps

        db.commit()
    finally:
        db.close()
