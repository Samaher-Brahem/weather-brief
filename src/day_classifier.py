from datetime import datetime
from config import COMMUTE_DAYS
from src.holidays import is_today_holiday


def get_day_type() -> str:
    """
    Determines what type of day today is:
    - "holiday" → Belgian public holiday
    - "weekend" → Saturday or Sunday
    - "commute_day" → Tuesday (1) or Thursday (3)
    - "work_from_home" → Other weekdays
    """
    
    today = datetime.now()
    weekday = today.weekday()  # Monday=0, Sunday=6
    
    # Check if holiday first
    if is_today_holiday():
        return "holiday"
    
    # Check if weekend
    if weekday >= 5:  # Saturday=5, Sunday=6
        return "weekend"
    
    # Check if commute day
    if weekday in COMMUTE_DAYS:
        return "commute_day"
    
    # Otherwise it's a regular work day (WFH or office)
    return "work_from_home"


def get_weather_hours(day_type: str) -> list:
    """
    Returns which hours to fetch weather for based on day type.
    """
    from config import MORNING_HOURS, MIDDAY_HOURS, AFTERNOON_HOURS, FULL_DAY_HOURS
    
    if day_type == "holiday" or day_type == "weekend":
        return FULL_DAY_HOURS
    elif day_type == "commute_day":
        # Show commute hours + lunch + afternoon
        return MORNING_HOURS + MIDDAY_HOURS + AFTERNOON_HOURS
    else:  # work_from_home
        return FULL_DAY_HOURS