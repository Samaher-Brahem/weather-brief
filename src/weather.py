"""Weather data fetching and parsing utilities."""
import sys
from pathlib import Path
import requests

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CITIES

WMO_CODES = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "foggy", 48: "icy fog",
    51: "light drizzle", 53: "drizzle", 55: "heavy drizzle",
    61: "light rain", 63: "rain", 65: "heavy rain",
    71: "light snow", 73: "snow", 75: "heavy snow",
    77: "snow grains",
    80: "light showers", 81: "showers", 82: "violent showers",
    85: "snow showers", 86: "heavy snow showers",
    95: "thunderstorm", 96: "thunderstorm with hail", 99: "thunderstorm with heavy hail"
}


def fetch_forecast(city_key: str) -> dict:
    """Fetch hourly forecast from Open-Meteo API."""
    city = CITIES[city_key]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": city["lat"],
        "longitude": city["lon"],
        "hourly": "temperature_2m,precipitation_probability,weathercode,windspeed_10m,apparent_temperature",
        "forecast_days": 1,
        "timezone": "Europe/Brussels"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def extract_hours(data: dict, hours: list) -> list:
    """Extract weather data for specific hours."""
    hourly = data["hourly"]
    result = []
    for i, time_str in enumerate(hourly["time"]):
        hour = int(time_str.split("T")[1].split(":")[0])
        if hour in hours:
            result.append({
                "hour": f"{hour:02d}:00",
                "temp": round(hourly["temperature_2m"][i]),
                "feels_like": round(hourly["apparent_temperature"][i]),
                "condition": WMO_CODES.get(hourly["weathercode"][i], "unknown"),
                "rain_prob": hourly["precipitation_probability"][i],
                "wind_kmh": round(hourly["windspeed_10m"][i])
            })
    return result


def get_period_summary(snapshots: list) -> dict:
    """Get aggregated weather stats for a period (morning/midday/evening)."""
    if not snapshots:
        return {}
    
    temps = [s["temp"] for s in snapshots]
    rain_probs = [s["rain_prob"] for s in snapshots]
    winds = [s["wind_kmh"] for s in snapshots]
    
    return {
        "min_temp": min(temps),
        "max_temp": max(temps),
        "avg_rain_prob": round(sum(rain_probs) / len(rain_probs)),
        "avg_wind": round(sum(winds) / len(winds)),
        "conditions": [s["condition"] for s in snapshots],
        "primary_condition": snapshots[0]["condition"]  # Most representative
    }


def get_city_forecast(city_key: str, hour_slots: list) -> str:
    """Get formatted forecast string for specific hours."""
    raw_data = fetch_forecast(city_key)
    snapshots = extract_hours(raw_data, hour_slots)
    return "\n".join(
        f"* {s['hour']}: {s['condition']}, {s['temp']}°C (feels like {s['feels_like']}°C), "
        f"rain {s['rain_prob']}%, wind {s['wind_kmh']} km/h"
        for s in snapshots
    )


def get_city_temp_range(city_key: str, hour_slots: list) -> tuple[int, int]:
    """Get min/max temperatures for specific hours."""
    raw_data = fetch_forecast(city_key)
    snapshots = extract_hours(raw_data, hour_slots)
    temps = [s["temp"] for s in snapshots]
    return min(temps), max(temps)


def get_period_summaries(city_key: str, periods: dict) -> dict:
    """Get weather summaries for all periods (morning/midday/evening)."""
    raw_data = fetch_forecast(city_key)
    summaries = {}
    for period_name, hours in periods.items():
        snapshots = extract_hours(raw_data, hours)
        summaries[period_name] = get_period_summary(snapshots)
    return summaries