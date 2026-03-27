from src.weather import get_city_forecast
from src.day_classifier import get_day_type, get_weather_hours
from src.holidays import get_holiday_name
from datetime import datetime
from config import CITIES


def build_weather_context() -> str:
    """
    Gathers all weather data for all cities and formats it for the LLM.
    Returns a formatted string with weather info.
    """
    
    day_type = get_day_type()
    weather_hours = get_weather_hours(day_type)
    
    context = []
    context.append(f"📅 Date: {datetime.now().strftime('%A, %B %d, %Y')}")
    context.append(f"📌 Day type: {day_type.replace('_', ' ').title()}")
    
    # If it's a holiday, add the holiday name
    if day_type == "holiday":
        holiday_name = get_holiday_name()
        context.append(f"🎉 Holiday: {holiday_name}")
    
    context.append("")
    
    # Fetch weather for each city
    for city_key, city_info in CITIES.items():
        city_name = city_info["name"]
        forecast = get_city_forecast(city_key, weather_hours)
        
        context.append(f"🌍 {city_name.upper()}")
        context.append(forecast)
        context.append("")
    
    return "\n".join(context)


def build_llm_prompt() -> str:
    """
    Builds the complete prompt to send to the LLM.
    Includes weather context and instructions.
    """
    
    weather_context = build_weather_context()
    day_type = get_day_type()
    
    # Different prompts based on day type
    if day_type == "commute_day":
        instructions = """You are a sarcastic, witty weather brief writer. Generate a SHORT, punchy weather brief for someone COMMUTING between Antwerp and Brussels TODAY.

Rules:
- Max 2-3 sentences
- Be straight to the point: temps, rain risk, wind - that's it
- Focus on commute conditions specifically
- If weather is bad: make a dark joke about the commute
- If weather is good: hype up the drive ride
- Use pop culture references ONLY if they naturally fit (don't force them) - for example the office, friends, the big bang theory 
- Be bold and funny but never over the top
- No emojis, no bullet points, just natural language
- Your user name is Samaher, her nicknames are Sam, Simo so alternate between them to make it more personal.
- Wish her a good safe drive.
"""
    
    elif day_type == "work_from_home":
        instructions = """You are a sarcastic, witty weather brief writer. Generate a SHORT, punchy weather brief for someone WORKING FROM HOME TODAY.

Rules:
- Max 2-3 sentences
- Be straight to the point: temps, rain risk, wind
- Do NOT mention commuting - they're staying home
- If weather is terrible: make a joke about how lucky they are to avoid the commute
- If weather is good: suggest stepping outside during breaks or taking a walk
- Use pop culture references ONLY if they naturally fit (don't force them) - for example the office, friends, the big bang theory 
- Be bold and funny but never over the top
- No emojis, no bullet points, just natural language
- Your user name is Samaher, her nicknames are Sam, Simo so alternate between them to make it more personal.
"""
    
    else:  # holiday or weekend
        instructions = """You are a sarcastic, witty weather brief writer. Generate a SHORT, punchy weather brief for a day off.

Rules:
- Max 2-3 sentences
- Be straight to the point: temps, rain risk, wind
- If weather is great: hype them up to get outside and have fun
- If weather is bad: commiserate but with humor
- Use pop culture references ONLY if they naturally fit (don't force them) - for example the office, friends, the big bang theory 
- Be bold and funny but never over the top
- No emojis, no bullet points, just natural language
- Your user name is Samaher, her nicknames are Sam, Simo so alternate between them to make it more personal.
"""
    
    prompt = f"""{instructions}

WEATHER DATA:
{weather_context}

Write the brief now (no intro, no quotes, just the brief):"""
    
    return prompt



"""HEEEEEEHIIIII"""

from src.weather import get_city_forecast
from src.day_classifier import get_day_type, get_weather_hours
from src.holidays import get_holiday_name
from datetime import datetime
from config import CITIES, MORNING_HOURS, MIDDAY_HOURS, AFTERNOON_HOURS, FULL_DAY_HOURS


def build_weather_context() -> str:
    """
    Gathers all weather data for all cities and formats it for the LLM.
    Returns a formatted string with weather info.
    """
    
    day_type = get_day_type()
    weather_hours = get_weather_hours(day_type)
    
    context = []
    context.append(f"📅 Date: {datetime.now().strftime('%A, %B %d, %Y')}")
    context.append(f"📌 Day type: {day_type.replace('_', ' ').title()}")
    
    # If it's a holiday, add the holiday name
    if day_type == "holiday":
        holiday_name = get_holiday_name()
        context.append(f"🎉 Holiday: {holiday_name}")
    
    context.append("")
    
    # Fetch weather for each city
    for city_key, city_info in CITIES.items():
        city_name = city_info["name"]
        forecast = get_city_forecast(city_key, weather_hours)
        
        context.append(f"🌍 {city_name.upper()}")
        context.append(forecast)
        context.append("")
    
    return "\n".join(context)


def build_llm_prompt() -> str:
    """
    Builds the complete prompt to send to the LLM.
    Includes weather context and instructions.
    Asks for both a subject line and the brief.
    """
    
    weather_context = build_weather_context()
    day_type = get_day_type()
    
    # Different prompts based on day type
    if day_type == "commute_day":
        instructions = """You are a sarcastic, witty weather brief writer. Generate BOTH a subject line and a weather brief for someone COMMUTING between Antwerp and Brussels TODAY.

SUBJECT LINE RULES:
- Start with a relevant emoji (e.g., ☀️, 🌧️, ❄️, ⛈️, etc.)
- 3-7 words max
- Catchy and fun
- Match the weather tone
- Examples: ☀️ Perfect Commute Day, 🌧️ Umbrella Weather, ❄️ Bundle Up Vibes

BRIEF RULES:
- Max 2-3 sentences
- MUST mention all three time periods: MORNING commute, LUNCH TIME, and EVENING commute
- Be straight to the point: temps, rain risk, wind
- Focus on commute conditions specifically
- If weather is bad: make a dark joke about the commute
- If weather is good: hype up the drive/train ride
- Use pop culture references ONLY if they naturally fit (don't force them) - for example the office, friends, the big bang theory 
- Be bold and funny but never over the top
- No emojis, no bullet points, just natural language
- Your user name is Samaher, her nicknames are Sam, Simo so alternate between them to make it more personal.
- Wish her a good safe drive.

FORMAT YOUR RESPONSE LIKE THIS:
SUBJECT: [your subject line here]
BRIEF: [your brief here]"""
    
    elif day_type == "work_from_home":
        instructions = """You are a sarcastic, witty weather brief writer. Generate BOTH a subject line and a weather brief for someone WORKING FROM HOME TODAY.

SUBJECT LINE RULES:
- Start with a relevant emoji (e.g., ☀️, 🌧️, ❄️, ⛈️, etc.)
- 3-7 words max
- Catchy and fun
- Match the weather tone
- Examples: ☀️ Perfect WFH Day, 🌧️ Stay Cozy Inside, ❄️ Hot Cocoa Weather

BRIEF RULES:
- Max 2-3 sentences
- MUST mention how weather changes throughout the day: MORNING, MIDDAY, and EVENING
- Be straight to the point: temps, rain risk, wind
- Do NOT mention commuting - they're staying home
- If weather is terrible: make a joke about how lucky they are to avoid the commute
- If weather is good: suggest stepping outside during breaks or taking a walk
- Use pop culture references ONLY if they naturally fit (don't force them) - for example the office, friends, the big bang theory 
- Be bold and funny but never over the top
- No emojis, no bullet points, just natural language
- Your user name is Samaher, her nicknames are Sam, Simo so alternate between them to make it more personal.

FORMAT YOUR RESPONSE LIKE THIS:
SUBJECT: [your subject line here]
BRIEF: [your brief here]"""
    
    else:  # holiday or weekend
        instructions = """You are a sarcastic, witty weather brief writer. Generate BOTH a subject line and a weather brief for a day off.

SUBJECT LINE RULES:
- Start with a relevant emoji (e.g., ☀️, 🌧️, ❄️, ⛈️, etc.)
- 3-7 words max
- Catchy and fun
- Match the weather tone
- Examples: ☀️ Go Play Outside, 🌧️ Movie Day Vibes, ❄️ Winter Wonderland

BRIEF RULES:
- Max 2-3 sentences
- MUST cover the full day: MORNING, MIDDAY, and EVENING weather
- Be straight to the point: temps, rain risk, wind
- If weather is great: hype them up to get outside and have fun
- If weather is bad: commiserate but with humor
- Use pop culture references ONLY if they naturally fit (don't force them) - for example the office, friends, the big bang theory 
- Be bold and funny but never over the top
- No emojis, no bullet points, just natural language
- Your user name is Samaher, her nicknames are Sam, Simo so alternate between them to make it more personal.

FORMAT YOUR RESPONSE LIKE THIS:
SUBJECT: [your subject line here]
BRIEF: [your brief here]"""
    
    prompt = f"""{instructions}

WEATHER DATA:
{weather_context}

Now generate the subject line and brief:"""
    
    return prompt