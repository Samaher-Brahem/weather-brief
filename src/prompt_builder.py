"""Prompt builder for weather brief generation."""
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CITIES
from src.day_classifier import get_weather_hours, get_day_type
from src.weather import get_period_summaries, get_city_temp_range


def build_weather_context(day_type: str) -> tuple[str, dict]:
    """
    Build the weather context header and summaries.
    
    Returns:
        Tuple of (header_html, weather_summaries)
    """
    city_key = "antwerp"
    weather_hours = get_weather_hours(day_type)
    all_hours = [hour for hours in weather_hours.values() for hour in hours]
    
    min_temp, max_temp = get_city_temp_range(city_key, all_hours)
    date_str = datetime.now().strftime("%A, %B %d")
    day_of_week = datetime.now().strftime("%A")
    
    summaries = get_period_summaries(city_key, weather_hours)
    
    # Add metadata to summaries
    for summary in summaries.values():
        summary["day_of_week"] = day_of_week
    
    header = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="margin: 0 0 10px 0;">{date_str}</h2>
        <p style="margin: 5px 0;">🌡️ High: {max_temp}°C | Low: {min_temp}°C</p>
    </div>
    """
    
    return header, summaries


def build_llm_prompt(day_type: str, summaries: dict) -> str:
    """
    Build an optimized LLM prompt focused on period-based summaries.
    
    Args:
        day_type: Type of day (holiday, weekend, commute_day, work_from_home)
        summaries: Weather summaries for each period
        
    Returns:
        Formatted prompt string
    """
    morning = summaries.get("morning", {})
    midday = summaries.get("midday", {})
    evening = summaries.get("evening", {})
    
    # Format weather data for prompt
    morning_info = f"{morning.get('min_temp', '-')}°C-{morning.get('max_temp', '-')}°C, {morning.get('avg_rain_prob', 0)}% rain, {morning.get('avg_wind', 0)} km/h wind"
    midday_info = f"{midday.get('min_temp', '-')}°C-{midday.get('max_temp', '-')}°C, {midday.get('avg_rain_prob', 0)}% rain, {midday.get('avg_wind', 0)} km/h wind"
    evening_info = f"{evening.get('min_temp', '-')}°C-{evening.get('max_temp', '-')}°C, {evening.get('avg_rain_prob', 0)}% rain, {evening.get('avg_wind', 0)} km/h wind"
    
    base_prompt = f"""You are a friendly, casual weather brief writer. Write a concise weather brief for Antwerp today.

WEATHER DATA:
- Morning: {morning_info}
- Midday: {midday_info}
- Evening: {evening_info}

INSTRUCTIONS:
1. Start with "Hi Sam," - a warm greeting
2. Write 1-2 friendly sentences for each period (Morning, Midday, Evening)
3. Keep language casual and conversational
4. IMPORTANT: NO hourly breakdowns - summarize each period as a whole
5. If there's a notable weather change (e.g., rain clearing up), highlight it
6. Add ONE practical tip or encouraging closing line (e.g., "Perfect for a walk!", "Bring an umbrella", "Stay cozy!")
7. No bullet points - use flowing paragraphs

FORMAT:
Hi Sam,

Morning: [1-2 sentences about morning conditions]

Midday: [1-2 sentences about midday conditions]

Evening: [1-2 sentences about evening conditions]

[1 sentence tip or closing wish - something cozy or encouraging]

Keep it under 150 words total. Be warm, witty, and conversational."""

    return base_prompt