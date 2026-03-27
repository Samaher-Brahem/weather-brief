import requests
from config import CITIES

# maps open-meteo weather codes → readable text
WMO_CODES = {
    0: "clear sky",
    1: "mainly clear", 2: "partly cloudy", 3: "overcast",
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
    """
    Calls Open-Meteo API and returns raw hourly forecast data.
    No API key needed.
    """

    city = CITIES[city_key]

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": city["lat"],
        "longitude": city["lon"],
        "hourly": ",".join([  # IMPORTANT: must be a string
            "temperature_2m",
            "precipitation_probability",
            "weathercode",
            "windspeed_10m",
            "apparent_temperature"
        ]),
        "forecast_days": 1,
        "timezone": "Europe/Brussels"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


def extract_hours(data: dict, hours: list) -> list:
    """
    Extracts only the hours we care about from the 24h dataset.
    Returns structured snapshots.
    """

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


def format_snapshot(snapshots: list) -> str:
    """
    Converts structured data into a readable string.
    This is what you'll pass to your LLM later.
    """

    lines = []

    for s in snapshots:
        lines.append(
            f"{s['hour']}: {s['condition']}, {s['temp']}°C "
            f"(feels like {s['feels_like']}°C), "
            f"rain probability {s['rain_prob']}%, "
            f"wind {s['wind_kmh']} km/h"
        )

    return "\n".join(lines)


def get_city_forecast(city_key: str, hour_slots: list) -> str:
    """
    Main function used by the rest of the app.

    Example:
    get_city_forecast("antwerp", MORNING_HOURS)
    """

    raw_data = fetch_forecast(city_key)
    snapshots = extract_hours(raw_data, hour_slots)

    return format_snapshot(snapshots)