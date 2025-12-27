from datetime import date
from models.workout import Workout
from models.workout_set import WorkoutSet
from mcp.exercise_resolver import resolve_exercise
from ai.schemas import ParsedWorkout

def build_workout(db, user_id, parsed_workout: ParsedWorkout):
  workout = Workout(
    user_id=user_id,
    date=parsed_workout.date or date.today(),
    notes=parsed_workout.notes,
  )
  db.add(workout)
  db.commit()
  db.refresh(workout)
  
  created_exercises = []

  for ex in parsed_workout.exercises:
    exercise, created = resolve_exercise(db, ex)

    for _ in range(ex.sets):
      ws = WorkoutSet(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=ex.reps,
        weight=ex.weight,
        rpe=ex.rest_time,
      )
      db.add(ws)
      
      if created:
        created_exercises.append({
          "name": ex.name,
          "confidence": ex.confidence,
        })
  db.commit()
  return workout, created_exercises
  