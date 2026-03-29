"""weather api interactions."""
import requests
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
    # 7 am to 9 pm (index 7 to 21)
    day_rains = hourly["precipitation_probability"][7:22]
    return max(day_rains) if day_rains else 0

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