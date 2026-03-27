from src.weather import get_city_forecast
from src.day_classifier import get_day_type, get_weather_hours
from src.holidays import get_holiday_name
from src.prompts import COMMUTE_DAY_PROMPT, WFH_DAY_PROMPT, HOLIDAY_WEEKEND_PROMPT
from datetime import datetime
from config import CITIES, USER_NAMES, COMMUTE_BOOSTS
import random


def build_weather_context(day_type: str) -> str:
    """
    Gathers weather data for relevant cities based on day type.
    Returns a formatted string with weather info.
    """
    
    weather_hours = get_weather_hours(day_type)
    
    context = []
    context.append(f"📅 Date: {datetime.now().strftime('%A, %B %d, %Y')}")
    context.append(f"📌 Day type: {day_type.replace('_', ' ').title()}")
    
    # If it's a holiday, add the holiday name
    if day_type == "holiday":
        holiday_name = get_holiday_name()
        context.append(f"🎉 Holiday: {holiday_name}")
    
    context.append("")
    
    # Determine which cities to show based on day type
    if day_type == "commute_day":
        # Show both cities for commute days
        cities_to_show = ["antwerp", "brussels"]
    else:
        # Only show Antwerp for WFH/holiday/weekend
        cities_to_show = ["antwerp"]
    
    # Fetch weather for relevant cities
    for city_key in cities_to_show:
        city_info = CITIES[city_key]
        city_name = city_info["name"]
        forecast = get_city_forecast(city_key, weather_hours)
        
        context.append(f"🌍 {city_name.upper()}")
        context.append(forecast)
        context.append("")
    
    return "\n".join(context)



def get_commute_boost() -> str:
    """
    Returns a random motivational phrase for commute days.
    """
    return random.choice(COMMUTE_BOOSTS)


def build_llm_prompt() -> str:
    """
    Builds the complete prompt to send to the LLM.
    Includes weather context and instructions.
    """
    
    day_type = get_day_type()
    weather_context = build_weather_context(day_type)
    
    # Select the appropriate prompt template
    if day_type == "commute_day":
        base_prompt = COMMUTE_DAY_PROMPT
        boost = get_commute_boost()
        # Add the boost phrase to the prompt
        base_prompt = base_prompt.replace(
            "END with a motivational/inspirational one-liner",
            f"END with this motivational phrase: '{boost}'"
        )
    elif day_type == "work_from_home":
        base_prompt = WFH_DAY_PROMPT
    else:  # holiday or weekend
        base_prompt = HOLIDAY_WEEKEND_PROMPT
    
    prompt = f"""{base_prompt}

WEATHER DATA:{weather_context} Now generate the subject line and brief:"""
    
    return prompt