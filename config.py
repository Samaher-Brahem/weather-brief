# =========================
# 📍 Cities configuration
# =========================

CITIES = {
    "antwerp": {
        "lat": 51.2194,
        "lon": 4.4025,
        "name": "Antwerp"
    },
    "brussels": {
        "lat": 50.8503,
        "lon": 4.3517,
        "name": "Brussels"
    }
}


# =========================
# ⏰ Time slots
# =========================

# Morning commute (leaving home)
MORNING_HOURS = [7, 8, 9]

# Lunch time (at work)
MIDDAY_HOURS = [12, 13]

# After work / commute back
AFTERNOON_HOURS = [17, 18, 19]

# General day overview (weekends / holidays / WFH)
FULL_DAY_HOURS = [9, 12, 15, 18]


# =========================
# 🗓️ Work logic
# =========================

# Tuesday (1) and Thursday (3) — Python weekday(): Monday = 0
COMMUTE_DAYS = [1, 3]


# =========================
# 🇧🇪 Public holidays
# =========================

# Official Belgian holidays Google Calendar ID
# BELGIAN_HOLIDAYS_CALENDAR_ID = "belgian.calendar.id@group.calendar.google.com"