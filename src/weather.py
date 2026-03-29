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
    """fetch a weather GIF with hardened validation for GitHub Actions."""
    api_key = os.getenv("GIPHY_API_KEY")
    
    # Your verified stable fallback
    fallback_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExemdteWFpanhuNDFzbmhvbTg0ZW9haThpYzFzeTRmNnUzajNxZno1byZlcD12MV9naWZzX3NlYXJjaCZjdD1n/AEpaVDTAop4TC/giphy.gif"
    
    if not api_key:
        return fallback_url

    query = f"{condition} weather"
    url = "https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": api_key,
        "q": query,
        "limit": 10,  # Increased limit to provide better selection
        "rating": "g"
    }
    
    # Add a User-Agent to look less like a bot when running from GitHub data centers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=5).json()
        if resp.get('data') and len(resp['data']) > 0:
            # Shuffle and try to find a URL that isn't an error placeholder
            choices = resp['data']
            random.shuffle(choices)
            
            for choice in choices:
                gif_url = choice['images']['downsized_medium']['url'].split('?')[0]
                
                # HARDENED VALIDATION: 
                # 1. Must be a direct media link
                # 2. Must not contain common Giphy error IDs (404, errors, etc)
                if "media" in gif_url and all(x not in gif_url for x in ["/404/", "/errors/", "/error-"]):
                    return gif_url
                    
    except Exception as e:
        print(f"⚠️ GIF Error: {e}")
    
    # If the API returned junk or failed, use the reliable fallback
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