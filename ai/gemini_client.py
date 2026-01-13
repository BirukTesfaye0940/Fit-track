import google.generativeai as genai
from ai.schemas import ParsedWorkout
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_text(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()

def parse_workout_text(text: str) -> ParsedWorkout:
  prompt = f"""
You are a fitness assistant. Parse the workout text into structured JSON matching this exact schema:

{{
  "date": "YYYY-MM-DD" or null,
  "duration_minutes": number or null,
  "mood": "mood description" or null,
  "notes": "any remaining text or additional notes" or null,
  "exercises": [
    {{
      "name": "exercise name",
      "muscle_group": "inferred muscle group (REQUIRED)",
      "equipment": "inferred equipment (REQUIRED)",
      "sets": number,
      "reps": number,
      "weight": number (in kg) or null,
      "rpe": number (1-10) or null,
      "confidence": number (0.0-1.0)
    }}
  ]
}}

Rules:
- Output ONLY valid JSON matching the schema above
- Extract "duration_minutes" if mentioned (e.g. "45 mins", "1 hour")
- Extract "mood" description if mentioned (e.g. "feeling great", "tired but pushed through")
- Put all remaining non-parsed text into "notes"
- Do NOT wrap in markdown code fences
- Do not invent exercises
- Confidence between 0 and 1 (1.0 = certain)
- If date is not mentioned, use null
- ALWAYS infer muscle group and equipment from the exercise name (e.g. "Bench Press" -> "Chest", "Barbell")

Workout text:
{text}
  """
  response = model.generate_content(prompt)
  
  # Strip markdown code fences if present
  json_text = response.text.strip()
  if json_text.startswith("```"):
    # Remove opening fence
    json_text = json_text.split("\n", 1)[1] if "\n" in json_text else json_text[3:]
    # Remove closing fence
    if json_text.endswith("```"):
      json_text = json_text.rsplit("\n```", 1)[0]
  
  return ParsedWorkout.model_validate_json(json_text)

def weekly_coach_feedback(signals: dict) -> str:
  prompt = f"""
    You are a professional strength and conditioning coach.

Here is the user's weekly training summary:
{signals}

Your task:
- Give a concise weekly review
- Point out positives
- Identify risks or gaps
- Suggest 1–2 improvements for next week

Rules:
- No medical advice
- Be practical and encouraging
- Max 50 words
"""
  return generate_text(prompt)