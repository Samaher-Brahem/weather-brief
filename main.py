"""

from src.weather import get_city_forecast
from config import MORNING_HOURS, AFTERNOON_HOURS

if __name__ == "__main__":
    print("=== ANTWERP MORNING ===")
    print(get_city_forecast("antwerp", MORNING_HOURS))

    print("\n=== BRUSSELS EVENING ===")
    print(get_city_forecast("brussels", AFTERNOON_HOURS))


from src.day_classifier import classify_day

if __name__ == "__main__":
    # temporary: simulate NOT a holiday
    day = classify_day(is_holiday=False)
    print(day)



from src.holidays import is_today_holiday
from src.day_classifier import classify_day

if __name__ == "__main__":
    today_holiday = is_today_holiday()
    day = classify_day(is_holiday=today_holiday)
    print("Is today a holiday?", today_holiday)
    print("Day classification:", day)

    

from src.day_classifier import get_day_type, get_weather_hours

# Test day classifier
day_type = get_day_type()
weather_hours = get_weather_hours(day_type)

print(f"Today's day type: {day_type}")
print(f"Weather hours to fetch: {weather_hours}")



from src.prompt_builder import build_llm_prompt

# Test prompt builder
prompt = build_llm_prompt()
print(prompt)



from src.prompt_builder import build_llm_prompt
from src.llm_client import generate_weather_brief

# Build the prompt
prompt = build_llm_prompt()

print("=" * 50)
print("WEATHER BRIEF")
print("=" * 50)

# Generate the brief (this already prints during streaming)
brief = generate_weather_brief(prompt)
"""

from src.prompt_builder import build_llm_prompt
from src.llm_client import generate_weather_brief
from src.email_sender import send_weather_brief_email
from datetime import datetime
import pytz

# Add this at the start of main.py
brussels_tz = pytz.timezone('Europe/Brussels')
now = brussels_tz.localize(datetime.now())

# Only run between 6:00 AM and 7:00 AM Brussels time
if not (6 <= now.hour < 7):
    print("Not the right time, skipping...")
    exit(0)

# Build the prompt
prompt = build_llm_prompt()

print("=" * 50)
print("GENERATING WEATHER BRIEF")
print("=" * 50)

# Generate the brief (returns tuple of subject and brief)
subject, brief = generate_weather_brief(prompt)

print("=" * 50)
print("SENDING EMAIL")
print("=" * 50)

# Send via email
send_weather_brief_email(subject, brief)