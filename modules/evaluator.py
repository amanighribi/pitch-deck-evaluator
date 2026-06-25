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

    # Detect template/placeholder content
    placeholder_keywords = [
        "your company name", "your one-sentence", "founder name",
        "funding round", "pain point #1", "pain point #2",
        "key feature #1", "revenue stream #1", "competitor a",
        "founder@yourcompany", "www.yourcompany", "xx,xxx", "$xxxk"
    ]

    text_lower = deck_text.lower()
    placeholder_count = sum(1 for kw in placeholder_keywords if kw in text_lower)

    if placeholder_count >= 3:
        return {
            "error": "This appears to be an empty template with placeholder text. Please upload a completed pitch deck with real content."
        }

    prompt = build_prompt(deck_text)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
    except Exception:
        return {
            "error": "Could not connect to the AI service. Please check your API key and try again."
        }

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        result = json.loads(raw)
        return result
    except json.JSONDecodeError:
        return {
            "error": "The AI returned an unexpected response. Please try again."
        }