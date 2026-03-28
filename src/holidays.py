"""Holiday detection utilities."""
from datetime import datetime
import requests

ICS_URL = "https://www.officeholidays.com/ics-all/belgium"

# Cache for holidays to avoid repeated API calls
_holiday_cache = None


def _fetch_holidays() -> list:
    """Fetch Belgian public holidays from officeholidays.com."""
    try:
        response = requests.get(ICS_URL, timeout=10)
        response.raise_for_status()
        lines = response.text.splitlines()
        holidays = []
        current_date = None
        current_name = None

        for line in lines:
            if line.startswith("DTSTART"):
                try:
                    current_date = datetime.strptime(line.split(":")[1].strip(), "%Y%m%d").date()
                except Exception:
                    current_date = None
            elif line.startswith("SUMMARY"):
                current_name = line.split(":", 1)[1].strip()
                if current_date and current_name and "Not a Public Holiday" not in current_name:
                    holidays.append((current_date, current_name))
                current_date = None
                current_name = None
        return holidays
    except Exception as e:
        print(f"⚠️ Holiday fetch failed: {e}")
        return []


def is_today_public_holiday() -> bool:
    """Check if today is a Belgian public holiday."""
    today = datetime.now().date()
    holidays = _fetch_holidays()
    return any(date == today for date, _ in holidays)


def get_today_public_holiday_name() -> str:
    """Get the name of today's public holiday, if any."""
    today = datetime.now().date()
    holidays = _fetch_holidays()
    for date, name in holidays:
        if date == today:
            return name
    return None