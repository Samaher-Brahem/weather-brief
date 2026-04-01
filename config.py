"""configuration and constants."""
# locations
CITIES = {
    "antwerp": {"lat": 51.2194, "lon": 4.4025, "name": "Antwerp"},
    "brussels": {"lat": 50.8503, "lon": 4.3517, "name": "Brussels"},
}

# time slots (24h format)
OVERNIGHT_HOURS = list(range(0, 6))
MORNING_HOURS = list(range(6, 11))
MIDDAY_HOURS = list(range(11, 16))
EVENING_HOURS = list(range(16, 20))
NIGHT_HOURS = list(range(20, 24))

COMMUTE_DAYS = {1, 3}  # tuesday=1, thursday=3

# styling
#GRADIENT_COLOR_1 = "#667eea"
#GRADIENT_COLOR_2 = "#764ba2"
GRADIENT_COLOR_2 = "#34e89e"
GRADIENT_COLOR_1 = "#0f3443"
ACCENT_COLOR = "#667eea"
PERIOD_BOX_BG = "#f9f9f9"
PERIOD_BORDER_COLOR = "#667eea"