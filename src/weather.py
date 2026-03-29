"""weather api interactions."""
import requests
import os
import random
from config import CITIES

WMO_CODES = {
    0: "clear", 1: "mostly clear", 2: "partly cloudy", 3: "overcast",
    45: "fog", 48: "icy fog", 51: "light drizzle", 53: "drizzle", 
    61: "light rain", 63: "rain", 65: "heavy rain", 71: "light snow", 
    73: "snow", 95: "thunderstorm"
}

_forecast_cache = {}

def fetch_forecast(city_key: str) -> dict:
    if city_key in _forecast_cache: return _forecast_cache[city_key]
    city = CITIES[city_key]
    resp = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": city["lat"], "longitude": city["lon"],
        "hourly": "temperature_2m,precipitation_probability,weathercode,windspeed_10m",
        "forecast_days": 1, "timezone": "Europe/Brussels"
    }, timeout=5)
    resp.raise_for_status()
    _forecast_cache[city_key] = resp.json()["hourly"]
    return _forecast_cache[city_key]

def get_24h_temp_range(city_key: str) -> tuple[int, int]:
    hourly = fetch_forecast(city_key)
    temps = [round(t) for t in hourly["temperature_2m"][:24]]
    return min(temps), max(temps)

def get_daytime_rain_max(city_key: str) -> int:
    """get peak rain probability between 07:00 and 21:00."""
    hourly = fetch_forecast(city_key)
    day_rains = hourly["precipitation_probability"][7:22]
    return max(day_rains) if day_rains else 0

def get_weather_gif(condition: str) -> str:
    """fetch a weather GIF with hardened headers for GitHub Actions."""
    api_key = os.getenv("GIPHY_API_KEY")
    fallback_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExemdteWFpanhuNDFzbmhvbTg0ZW9haThpYzFzeTRmNnUzajNxZno1byZlcD12MV9naWZzX3NlYXJjaCZjdD1n/AEpaVDTAop4TC/giphy.gif"
    
    if not api_key:
        return fallback_url

    url = "https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": api_key,
        "q": f"{condition} weather",
        "limit": 10,
        "rating": "g"
    }
    
    # Fake a browser header to prevent Giphy from flagging GitHub Actions as a bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=5).json()
        if resp.get('data') and len(resp['data']) > 0:
            # Pick a random one from the top 10 for variety
            choice = random.choice(resp['data'])
            
            # 'original' is the most robust URL format for external embeds (emails)
            # .split('?')[0] is vital to remove tracking tokens that expire
            gif_url = choice['images']['original']['url'].split('?')[0]
            
            # Double check it's the direct media subdomain
            if "media" in gif_url or "giphy.gif" in gif_url:
                return gif_url
    except Exception as e:
        print(f"⚠️ GIF Fetch Error: {e}")
    
    return fallback_url

def get_period_summary(city_key: str, hours: list) -> dict:
    hourly = fetch_forecast(city_key)
    target_hours = set(hours)
    indices = [i for i, t in enumerate(hourly["time"]) if int(t.split("T")[1][:2]) in target_hours]
    if not indices: return {}
    
    temps = [hourly["temperature_2m"][i] for i in indices]
    rains = [hourly["precipitation_probability"][i] for i in indices]
    winds = [hourly["windspeed_10m"][i] for i in indices]
    
    return {
        "min_temp": round(min(temps)), "max_temp": round(max(temps)),
        "avg_rain": round(sum(rains) / len(rains)),
        "avg_wind": round(sum(winds) / len(winds)),
        "condition": WMO_CODES.get(hourly["weathercode"][indices[0]], "mixed")
    }