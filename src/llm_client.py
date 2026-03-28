"""Groq LLM client for weather brief generation."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

client = Groq()  # Uses GROQ_API_KEY from .env


def generate_weather_brief(prompt: str) -> str:
    """
    Generate weather brief text from the LLM.
    
    Args:
        prompt: The weather context and instructions
        
    Returns:
        Generated brief text
    """
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_completion_tokens=512,
        top_p=0.95,
        stream=True,
        stop=None
    )
    
    # Collect streamed response
    full_response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            full_response += content
    
    return full_response.strip()


def generate_subject_line(weather_summary: dict) -> str:
    """
    Generate a dynamic, emoji-rich subject line based on weather conditions.
    
    Args:
        weather_summary: Dictionary with weather stats (conditions, rain probability, etc.)
        
    Returns:
        Formatted subject line
    """
    conditions = weather_summary.get("conditions", [])
    rain_prob = weather_summary.get("avg_rain_prob", 0)
    max_temp = weather_summary.get("max_temp", 0)
    day_of_week = weather_summary.get("day_of_week", "Day")
    
    # Determine primary condition emoji
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
    
    # Add temperature indicator
    if max_temp < 0:
        temp_desc = "Freezing"
    elif max_temp < 10:
        temp_desc = "Cold"
    elif max_temp < 15:
        temp_desc = "Cool"
    elif max_temp < 20:
        temp_desc = "Pleasant"
    else:
        temp_desc = "Warm"
    
    return f"{emoji} {condition} {day_of_week} Ahead!"