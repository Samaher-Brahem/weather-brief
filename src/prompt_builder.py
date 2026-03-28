"""Prompt builder for weather brief generation."""
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CITIES, GRADIENT_COLOR_1, GRADIENT_COLOR_2
from src.day_classifier import get_weather_hours, get_day_type
from src.weather import get_period_summaries, get_city_temp_range


def get_locations_for_day(day_type: str) -> dict:
    """
    Determine which locations to use for each period based on day type.
    
    Returns:
        Dict with 'morning', 'midday', 'evening' mapped to city keys
    """
    if day_type == "commute_day":
        # Tuesday/Thursday: Antwerp morning, Brussels midday & evening, Antwerp evening
        return {
            "morning": "antwerp",
            "midday": "brussels",
            "evening": "antwerp"
        }
    else:
        # All other days: Antwerp only
        return {
            "morning": "antwerp",
            "midday": "antwerp",
            "evening": "antwerp"
        }


def build_weather_context(day_type: str) -> tuple[str, dict, dict]:
    """
    Build the weather context header and summaries with smart location selection.
    
    Returns:
        Tuple of (header_html, weather_summaries, locations_used)
    """
    weather_hours = get_weather_hours(day_type)
    locations = get_locations_for_day(day_type)
    
    # Get temperature range from Antwerp (for the header)
    all_hours = [hour for hours in weather_hours.values() for hour in hours]
    min_temp, max_temp = get_city_temp_range("antwerp", all_hours)
    
    date_str = datetime.now().strftime("%A, %B %d")
    day_of_week = datetime.now().strftime("%A")
    
    # Get summaries for each period from the appropriate city
    summaries = {}
    for period, city_key in locations.items():
        if period in weather_hours:
            period_summaries = get_period_summaries(city_key, {period: weather_hours[period]})
            if period in period_summaries:
                summaries[period] = period_summaries[period]
                summaries[period]["city"] = CITIES[city_key]["name"]
    
    # Add metadata
    for summary in summaries.values():
        summary["day_of_week"] = day_of_week
    
    header = f"""
    <div style="background: linear-gradient(135deg, {GRADIENT_COLOR_1} 0%, {GRADIENT_COLOR_2} 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="margin: 0 0 10px 0;">{date_str}</h2>
        <p style="margin: 5px 0;">🌡️ High: {max_temp}°C | Low: {min_temp}°C</p>
    </div>
    """
    
    return header, summaries, locations


def build_llm_prompt(day_type: str, summaries: dict, locations: dict) -> str:
    """
    Build an optimized LLM prompt with smart location and weather context.
    
    Args:
        day_type: Type of day (holiday, weekend, commute_day, work_from_home)
        summaries: Weather summaries for each period
        locations: Dict mapping periods to cities
        
    Returns:
        Formatted prompt string
    """
    morning = summaries.get("morning", {})
    midday = summaries.get("midday", {})
    evening = summaries.get("evening", {})
    
    morning_city = locations.get("morning", "antwerp").title()
    midday_city = locations.get("midday", "antwerp").title()
    evening_city = locations.get("evening", "antwerp").title()
    
    # Format weather data for prompt
    morning_info = f"{morning.get('min_temp', '-')}°C-{morning.get('max_temp', '-')}°C, {morning.get('avg_rain_prob', 0)}% rain, {morning.get('avg_wind', 0)} km/h wind ({morning_city})"
    midday_info = f"{midday.get('min_temp', '-')}°C-{midday.get('max_temp', '-')}°C, {midday.get('avg_rain_prob', 0)}% rain, {midday.get('avg_wind', 0)} km/h wind ({midday_city})"
    evening_info = f"{evening.get('min_temp', '-')}°C-{evening.get('avg_temp', '-')}°C, {evening.get('avg_rain_prob', 0)}% rain, {evening.get('avg_wind', 0)} km/h wind ({evening_city})"
    
    # Build context-aware prompt based on day type and weather
    is_good_weather = morning.get('avg_rain_prob', 100) < 40 and midday.get('avg_rain_prob', 100) < 40
    
    if day_type in ["weekend", "holiday"]:
        tone_instruction = "You're helping someone enjoy their day off."
        if is_good_weather:
            activity_hint = "Encourage outdoor activities since it's a nice day!"
        else:
            activity_hint = "Suggest cozy indoor activities since the weather isn't great."
    elif day_type == "work_from_home":
        tone_instruction = "You're helping someone working from home."
        activity_hint = "Mention if it's a good day to take breaks outside or stay cozy indoors."
    elif day_type == "commute_day":
        tone_instruction = "You're helping someone commuting between Antwerp and Brussels."
        activity_hint = "Note the weather differences between the two cities in midday."
    else:
        tone_instruction = "You're helping someone through their work day."
        activity_hint = "Give practical weather advice for the day."
    
    base_prompt = f"""You are a friendly, casual weather brief writer. {tone_instruction}

WEATHER DATA:
- Morning: {morning_info}
- Midday: {midday_info}
- Evening: {evening_info}

CONTEXT: {activity_hint}

INSTRUCTIONS:
1. Start with "Hi Sam," - a warm greeting
2. Write 1-2 friendly sentences for each period (Morning, Midday, Evening)
3. Keep language casual and conversational
4. IMPORTANT: NO hourly breakdowns - summarize each period as a whole
5. If there's a notable weather change (e.g., rain clearing up), highlight it
6. For commute days, note if Brussels weather differs from Antwerp
7. Add ONE practical tip or encouraging closing line based on the weather and day type
8. No bullet points - use flowing paragraphs

FORMAT:
Hi Sam,

Morning: [1-2 sentences about morning in {morning_city}]

Midday: [1-2 sentences about midday in {midday_city}]

Evening: [1-2 sentences about evening in {evening_city}]

[1 sentence tip or closing wish - cozy, encouraging, or activity suggestion]

Keep it under 150 words total. Be warm, witty, and conversational."""

    return base_prompt