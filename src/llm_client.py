"""Groq LLM client for weather brief generation."""
import os
import sys
from groq import Groq

# Optional: only for local dev (won’t break CI)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_groq_client():
    """Initialize Groq client with strict validation."""
    api_key = os.getenv("GROQ_API_KEY")

    # 🔍 Strong debug (safe, no key leak)
    if api_key:
        print(f"✅ GROQ_API_KEY loaded (length={len(api_key.strip())})")
    else:
        print("❌ GROQ_API_KEY is MISSING")

    # 🚨 Critical validation
    if not api_key or not api_key.strip():
        raise ValueError("GROQ_API_KEY is missing or empty")

    return Groq(api_key=api_key.strip())


def generate_weather_brief(prompt: str) -> str:
    """
    Generate weather brief text from the LLM.
    """
    client = get_groq_client()

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_completion_tokens=400,
            top_p=0.9,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print("❌ Groq API call failed:", str(e))
        raise


def generate_subject_line(weather_summary: dict) -> str:
    """Generate a dynamic subject line based on weather."""
    conditions = weather_summary.get("conditions", [])
    rain_prob = weather_summary.get("avg_rain_prob", 0)
    max_temp = weather_summary.get("max_temp", 0)
    day_of_week = weather_summary.get("day_of_week", "Day")

    condition_str = " ".join(conditions).lower()

    if rain_prob > 60:
        emoji = "🌧️"
        condition = "Rainy"
    elif rain_prob > 30:
        emoji = "🌦️"
        condition = "Partly Rainy"
    elif "cloud" in condition_str or "overcast" in condition_str:
        emoji = "☁️"
        condition = "Cloudy"
    elif "clear" in condition_str or "sunny" in condition_str:
        emoji = "☀️"
        condition = "Sunny"
    elif "snow" in condition_str:
        emoji = "❄️"
        condition = "Snowy"
    elif "fog" in condition_str:
        emoji = "🌫️"
        condition = "Foggy"
    else:
        emoji = "🌤️"
        condition = "Pleasant"

    return f"{emoji} {condition} {day_of_week} Ahead!"