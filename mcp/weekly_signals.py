from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.workout import Workout
from models.workout_set import WorkoutSet
from models.exercise import Exercise

def get_weekly_signals(db: Session, user_id):
  today = date.today()
  week_start = today - timedelta(days=7)

  workouts = (db.query(Workout).filter(
      Workout.user_id == user_id,
      Workout.date >= week_start
    ).all()
  )

  workout_ids = [w.id for w in workouts]
  if not workout_ids:
    return {
      "worked_out": False,
      "message": "No workouts logged this week"
    }
  
  sets = (db.query(
    Exercise.muscle_group,
    func.sum(WorkoutSet.reps * WorkoutSet.weight).label("volume"),
    func.avg(WorkoutSet.rpe).label("avg_rpe")
  )
  .join(WorkoutSet, WorkoutSet.exercise_id == Exercise.id)
  .filter(
    WorkoutSet.workout_id.in_(workout_ids)
  )
  .group_by(Exercise.muscle_group)
  .all()
  )

  volume_by_muscle = {
    muscle: int(volume)
    for muscle, volume, _ in sets
  }

  avg_rpe = round(
    sum(rpe for _, _, rpe in sets if rpe is not None) / len(sets),
    2
  ) if sets else None

  return {
    "worked_out": True,
    "volume_by_muscle": volume_by_muscle,
    "average_rpe": avg_rpe,
    "sessions": len(workouts)
  }

  