"""day type classification."""
from datetime import datetime
from zoneinfo import ZoneInfo
from src.holidays import is_today_public_holiday
from config import COMMUTE_DAYS, OVERNIGHT_HOURS, MORNING_HOURS, MIDDAY_HOURS, EVENING_HOURS, NIGHT_HOURS

def get_day_type() -> str:
    """determine if today is holiday, weekend, commute, or wfh."""
    weekday = now = datetime.now(ZoneInfo("Europe/Brussels")).weekday()
    
    if is_today_public_holiday():
        return "holiday"
    if weekday >= 5:
        return "weekend"
    if weekday in COMMUTE_DAYS:
        return "commute_day"
    return "work_from_home"

def get_weather_hours() -> dict:
    """return standard weather periods."""
    return {
        "overnight": OVERNIGHT_HOURS,
        "morning": MORNING_HOURS,
        "midday": MIDDAY_HOURS,
        "evening": EVENING_HOURS,
        "night": NIGHT_HOURS
    }