"""holiday caching and detection."""
from datetime import datetime
import requests
from zoneinfo import ZoneInfo


ICS_URL = "https://www.officeholidays.com/ics-all/belgium"
_holiday_cache = None

def _fetch_holidays() -> set:
    """fetch and cache holidays to avoid redundant api calls."""
    global _holiday_cache
    if _holiday_cache is not None:
        return _holiday_cache
        
    try:
        resp = requests.get(ICS_URL, timeout=5)
        resp.raise_for_status()
        
        holidays = set()
        current_date = None
        
        for line in resp.text.splitlines():
            if line.startswith("DTSTART"):
                try:
                    current_date = datetime.strptime(line.split(":")[1].strip(), "%Y%m%d").date()
                except ValueError:
                    continue
            elif line.startswith("SUMMARY") and current_date:
                if "Not a Public Holiday" not in line:
                    holidays.add(current_date)
                current_date = None
                
        _holiday_cache = holidays
        return holidays
    except Exception as e:
        print(f"⚠️ holiday fetch failed: {e}")
        return set()

def is_today_public_holiday() -> bool:
    """check if today is a public holiday."""
    return datetime.now(ZoneInfo("Europe/Brussels")).date() in _fetch_holidays()