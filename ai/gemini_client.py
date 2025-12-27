import os
import google.generativeai as genai
from ai.schemas import ParsedWorkout

genai.configure(api_key=os.getenv("AIzaSyD3zTX8u1DH08sxia5IiTyd4QIZY45rn-0"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")

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