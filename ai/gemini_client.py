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
    You are a fitness assistant.
Parse the workout text into structured JSON.

Rules:
- Output ONLY valid JSON
- Do not invent exercises
- Confidence between 0 and 1

Workout text:
{text}
  """
  response = model.generate_content(prompt)
  return ParsedWorkout.model_validate_json(response.text)

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
- Max 120 words
"""
  return generate_text(prompt)