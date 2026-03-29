"""context and prompt formulation."""
from datetime import datetime
from config import CITIES, GRADIENT_COLOR_1, GRADIENT_COLOR_2
from src.day_classifier import get_weather_hours
from src.weather import get_period_summary, get_24h_temp_range

def build_weather_context(day_type: str) -> tuple[str, dict]:
    """assemble weather data and html header."""
    periods = get_weather_hours()
    
    # smart routing based on commute
    locations = {p: "antwerp" for p in periods}
    if day_type == "commute_day":
        locations.update({"midday": "brussels", "evening": "brussels"})
        
    # compile summaries
    summaries = {}
    for period, hours in periods.items():
        city = locations[period]
        data = get_period_summary(city, hours)
        data["city"] = CITIES[city]["name"]
        summaries[period] = data
        
    # full day min/max based on antwerp
    min_temp, max_temp = get_24h_temp_range("antwerp")
    date_str = datetime.now().strftime("%A, %B %d")
    
    header = f"""
    <div style="background: linear-gradient(135deg, {GRADIENT_COLOR_1} 0%, {GRADIENT_COLOR_2} 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="margin: 0 0 10px 0;">{date_str}</h2>
        <p style="margin: 5px 0; font-size: 16px;">🌡️ High: {max_temp}°C | Low: {min_temp}°C</p>
    </div>
    """
    return header, summaries

def build_llm_prompt(day_type: str, summaries: dict) -> str:
    """build json-enforced llm prompt for structured line-by-line layout."""
    
    def fmt(p):
        s = summaries.get(p, {})
        # ensuring wind and specific data points are explicitly passed to the LLM
        return f"{s.get('min_temp')}°C-{s.get('max_temp')}°C, {s.get('avg_rain')}% rain, {s.get('avg_wind')} km/h wind, {s.get('condition')} ({s.get('city')})"

    return f"""You are a casual, down-to-earth weather assistant writing to Sam.
DAY TYPE: {day_type.replace('_', ' ')}
WEATHER DATA:
- Overnight (0-6h): {fmt('overnight')}
- Morning (6-11h): {fmt('morning')}
- Midday (11-16h): {fmt('midday')}
- Evening (16-20h): {fmt('evening')}
- Night (20-24h): {fmt('night')}

INSTRUCTIONS:
1. Output valid JSON only. No markdown formatting outside the JSON.
2. "subject": A dynamic, catchy subject line summarizing the general weather condition with an emoji.
3. "body": The email body exactly matching the structure below. Use double newlines (\\n\\n) between sections so it renders with line breaks.
4. Write natural sentences, but start each period explicitly with its name (e.g., "Morning: ").
5. Include the specific degrees, wind speeds, and rain probabilities naturally in the text.
6. Note that "Overnight" MUST be in the past tense (what happened while sleeping).
7. End with a casual, human sign-off (e.g., "Alright, peace out OR yo yo have a nice day OR ay besslema OR yalla peace OR yalla salem OR nharek zin, etc").

EXPECTED JSON FORMAT:
{{
  "subject": "emoji + catchy subject line",
  "body": "Good morning Sam,\\n\\n[1 sentence general vibe of the day]\\n\\nOvernight: [past tense, mention conditions and rain]\\n\\nMorning: [forecast, specific temps, wind, vibe]\\n\\nMidday: [forecast, specific temps, vibe]\\n\\nEvening: [forecast, temps, rain prob]\\n\\nNight: [forecast, temps, chill/dry note]\\n\\n[Casual sign-off]"
}}"""