"""context and prompt formulation."""
from datetime import datetime
from config import GRADIENT_COLOR_1, GRADIENT_COLOR_2, CITIES
from src.day_classifier import get_weather_hours
from src.weather import get_period_summary, get_24h_temp_range, get_daytime_rain_max, get_weather_gif

def build_weather_context(day_type: str) -> tuple[str, dict]:
    periods = get_weather_hours()
    locations = {p: "antwerp" for p in periods}
    if day_type == "commute_day":
        locations.update({"midday": "brussels", "evening": "brussels"})
        
    summaries = {p: {**get_period_summary(loc, periods[p]), "city": CITIES[loc]["name"]} 
                 for p, loc in locations.items()}
    
    min_temp, max_temp = get_24h_temp_range("antwerp")
    rain_chance = get_daytime_rain_max("antwerp")
    rain_label = "Low" if rain_chance < 20 else "Moderate" if rain_chance < 60 else "High"
    
    # We pass the GIF URL as part of the summaries or return it separately
    summaries['gif_url'] = get_weather_gif(summaries['midday']['condition'])
    
    header = f"""
    <div style="background: linear-gradient(135deg, {GRADIENT_COLOR_1} 0%, {GRADIENT_COLOR_2} 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="margin: 0 0 10px 0;">{datetime.now().strftime("%A, %B %d")}</h2>
        <p style="margin: 5px 0; font-size: 16px;">🌡️ High: {max_temp}°C | Low: {min_temp}°C</p>
        <p style="margin: 5px 0; font-size: 16px;">☔ Rain Risk: {rain_chance}% ({rain_label})</p>
    </div>
    """
    return header, summaries

def build_llm_prompt(day_type: str, summaries: dict) -> str:
    def fmt(p):
        s = summaries.get(p, {})
        return f"{s.get('min_temp')}°C-{s.get('max_temp')}°C, {s.get('avg_rain')}% rain, {s.get('avg_wind')}km/h wind, {s.get('condition')} ({s.get('city')})"

    return f"""You are WhetherAI, a witty weather assistant writing to Sam.
WEATHER DATA:
- Overnight (0-6h): {fmt('overnight')}
- Morning (6-11h): {fmt('morning')}
- Midday (11-16h): {fmt('midday')}
- Evening (16-20h): {fmt('evening')}
- Night (20-24h): {fmt('night')}

INSTRUCTIONS:
0. Start with a friendly morning to Sam or Samaher. Use a different greeting each time (you can be creative here).
1. Output valid JSON only. No markdown formatting outside the JSON.
2. "subject": A dynamic, catchy subject line summarizing the general weather condition with an emoji.
3. "body": The email body exactly matching the structure below. Use double newlines (\\n\\n) between sections so it renders with line breaks.
4. Write natural sentences, but start each period explicitly with its name (e.g., "Morning: ")
5. Include the specific degrees, wind speeds, and rain probabilities naturally in the text.
6. Note that "Overnight" MUST be in the past tense (what happened while sleeping).
7. End with a casual, human sign-off (e.g., "Alright, peace out OR yo yo have a nice day OR ay besslema OR yalla peace OR yalla salem OR nharek zin, etc").
8. You can be creative with the language and tone, but keep it concise and engaging. The goal is to make Sam smile while giving a clear picture of the day's weather.
9. Add your own punchy signature as WhetherAI (that's your name): "With love, WhetherAI" or "Your buddy, WhetherAI". 

EXPECTED JSON FORMAT:
{{
  "subject": "emoji + catchy subject line",
  "body": "morning greeting to Sam,\\n\\nTL;DR: [1 sentence general vibe of the day]\\n\\nOvernight: [past tense, mention conditions and rain]\\n\\nMorning: [forecast, specific temps, wind, vibe]\\n\\nMidday: [forecast, specific temps, vibe]\\n\\nEvening: [forecast, temps, rain prob]\\n\\nNight: [forecast, temps, chill/dry note]\\n\\n[Casual sign-off]\\n\\n[WhetherAI signature]"
}}"""