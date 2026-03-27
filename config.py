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
BELGIAN_HOLIDAYS_CALENDAR_ID = "en.be#holiday@group.v.calendar.google.com"


# =========================
# 👤 User preferences
# =========================

# User name for greetings (alternates between these)
USER_NAMES = ["Sam", "Samaher"]

# Motivational phrases for commute days
COMMUTE_BOOSTS = [
    "Remember: great things come with great effort.",
    "You've got this—every commute is a step forward.",
    "The grind pays off. Keep pushing.",
    "Excellence demands effort. Go earn it.",
    "You're stronger than you think. Let's go.",
    "Small consistent efforts lead to big wins.",
    "Stay focused, stay strong.",
    "Your effort today builds your tomorrow.",
]