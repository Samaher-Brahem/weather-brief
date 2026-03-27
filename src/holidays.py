from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

GOOGLE_CALENDAR_API_KEY = os.getenv("GOOGLE_CALENDAR_API_KEY")
BELGIAN_HOLIDAYS_CALENDAR_ID = "en.be#holiday@group.v.calendar.google.com"

# DEBUG: Check if key loaded
# print(f"API Key loaded: {GOOGLE_CALENDAR_API_KEY is not None}")
# print(f"API Key length: {len(GOOGLE_CALENDAR_API_KEY) if GOOGLE_CALENDAR_API_KEY else 0}")
# print(f"Calendar ID: {BELGIAN_HOLIDAYS_CALENDAR_ID}")


def is_today_holiday() -> bool:
    """
    Checks the official Belgian public holiday Google Calendar
    to see if today is a holiday.
    """

    today_str = datetime.now().strftime("%Y-%m-%d")

    # URL-encode the calendar ID
    encoded_calendar_id = quote(BELGIAN_HOLIDAYS_CALENDAR_ID, safe='')
    url = f"https://www.googleapis.com/calendar/v3/calendars/{encoded_calendar_id}/events"

    params = {
        "timeMin": f"{today_str}T00:00:00Z",
        "timeMax": f"{today_str}T23:59:59Z",
        "singleEvents": "true",
        "orderBy": "startTime",
        "key": GOOGLE_CALENDAR_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    events = data.get("items", [])

    return len(events) > 0


def get_holiday_name() -> str:
    """
    Returns the name of today's holiday, or None if not a holiday.
    """

    today_str = datetime.now().strftime("%Y-%m-%d")

    # URL-encode the calendar ID
    encoded_calendar_id = quote(BELGIAN_HOLIDAYS_CALENDAR_ID, safe='')
    url = f"https://www.googleapis.com/calendar/v3/calendars/{encoded_calendar_id}/events"

    params = {
        "timeMin": f"{today_str}T00:00:00Z",
        "timeMax": f"{today_str}T23:59:59Z",
        "singleEvents": "true",
        "orderBy": "startTime",
        "key": GOOGLE_CALENDAR_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    events = data.get("items", [])

    if len(events) > 0:
        return events[0]["summary"]  # Return the holiday name
    
    return None