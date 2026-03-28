"""Day type classification for weather briefing."""
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import COMMUTE_DAYS, MORNING_HOURS, MIDDAY_HOURS, EVENING_HOURS, FULL_DAY_HOURS
from src.holidays import is_today_public_holiday


def get_day_type() -> str:
    """Determine the type of day (holiday, weekend, commute, or work_from_home)."""
    today = datetime.now()
    weekday = today.weekday()  # Monday=0, Sunday=6

    if is_today_public_holiday():
        return "holiday"
    if weekday >= 5:  # Saturday=5, Sunday=6
        return "weekend"
    if weekday in COMMUTE_DAYS:
        return "commute_day"
    return "work_from_home"


def get_weather_hours(day_type: str) -> dict:
    """Get relevant weather hours for the day type."""
    return {
        "morning": MORNING_HOURS,
        "midday": MIDDAY_HOURS,
        "evening": EVENING_HOURS
    }