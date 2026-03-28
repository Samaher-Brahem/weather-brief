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
# On these days: Antwerp morning, Brussels midday & evening, Antwerp evening
COMMUTE_DAYS = [1, 3]

# User preferences
USER_NAME = "Sam"

# ===========================
# 🎨 EMAIL STYLING - Customize here!
# ===========================


# Gradient colors for header (change these to customize!)
GRADIENT_COLOR_1 = "#667eea"      # Left/start color (blue)
GRADIENT_COLOR_2 = "#764ba2"      # Right/end color (purple)

# Alternative color schemes you can use:
# 🌅 Sunrise: GRADIENT_COLOR_1 = "#FF6B6B", GRADIENT_COLOR_2 = "#FFA07A"
# 🌊 Ocean: GRADIENT_COLOR_1 = "#1E90FF", GRADIENT_COLOR_2 = "#00CED1"
# 🌿 Nature: GRADIENT_COLOR_1 = "#2ECC71", GRADIENT_COLOR_2 = "#27AE60"
# 🌙 Dark: GRADIENT_COLOR_1 = "#2C3E50", GRADIENT_COLOR_2 = "#34495E"
# 🎨 Warm: GRADIENT_COLOR_1 = "#FF6B35", GRADIENT_COLOR_2 = "#FF8C42"
# 💜 Purple: GRADIENT_COLOR_1 = "#9D4EDD", GRADIENT_COLOR_2 = "#5A189A"
# 🔥 Fire: GRADIENT_COLOR_1 = "#FF4500", GRADIENT_COLOR_2 = "#FF8C00"

# Accent color for section headers and highlights
ACCENT_COLOR = "#667eea"

# Background color for period boxes (Morning/Midday/Evening)
PERIOD_BOX_BG = "#f9f9f9"

# Border color for period boxes
PERIOD_BORDER_COLOR = "#667eea"

# Tip box background color
TIP_BOX_BG = "#e8f4f8"

# Tip box border color
TIP_BOX_BORDER = "#b3dfe8"

# Make period section headers (Morning, Midday, Evening) bold?
BOLD_PERIOD_HEADERS = True

# Period header styling
# Change to: "bold", "italic", or "bold-italic"
PERIOD_HEADER_STYLE = "bold"