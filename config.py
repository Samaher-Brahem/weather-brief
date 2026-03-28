# Weather Brief Configuration
# ===========================

# Cities configuration
CITIES = {
    "antwerp": {"lat": 51.2194, "lon": 4.4025, "name": "Antwerp"},
    "brussels": {"lat": 50.8503, "lon": 4.3517, "name": "Brussels"},
}

# Time slots for weather data
MORNING_HOURS = [7, 8, 9]
MIDDAY_HOURS = [12, 13]
EVENING_HOURS = [17, 18, 19]
FULL_DAY_HOURS = MORNING_HOURS + MIDDAY_HOURS + EVENING_HOURS

# Work commute days (Tuesday=1, Thursday=3)
COMMUTE_DAYS = [1, 3]

# User preferences
USER_NAME = "Sam"