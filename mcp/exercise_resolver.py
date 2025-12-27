from models.exercise import Exercise

def resolve_exercise(db, parsed):
  exercise = db.query(Exercise).filter(
    Exercise.name.ilike(parsed.name)
  ).first()

  created = False
  if not exercise:
    exercise = Exercise(
      name=parsed.name,
      muscle_group=parsed.muscle_group or "unknown",
      equipment=parsed.equipment or "unknown",
      ai_generated=True
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    created = True
  
  return exercise, created
      
      
  