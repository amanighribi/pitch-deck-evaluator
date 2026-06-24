import os
import json
from groq import Groq
from dotenv import load_dotenv
from modules.prompts import build_prompt

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def evaluate_deck(deck_text: str) -> dict:

    if not deck_text or len(deck_text.strip()) < 50:
        return {
            "error": "Unable to extract sufficient text from this PDF. It may be image-based and require OCR."
        }

    prompt = build_prompt(deck_text)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    result = json.loads(raw)
    return result