import requests
from datetime import datetime

# Melbourne coordinates
LATITUDE = -37.8136
LONGITUDE = 144.9631

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": [
        "temperature_2m",
        "apparent_temperature",
        "precipitation",
        "weather_code",
        "wind_speed_10m"
    ],
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_probability_max"
    ],
    "timezone": "Australia/Melbourne",
    "forecast_days": 1
}

response = requests.get(url, params=params, timeout=10)
response.raise_for_status()

data = response.json()

current = data["current"]
daily = data["daily"]

print("🌤 Melbourne Daily Weather")
print("-" * 35)
print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
print(f"Current temperature: {current['temperature_2m']} °C")
print(f"Feels like: {current['apparent_temperature']} °C")
print(f"Today's high: {daily['temperature_2m_max'][0]} °C")
print(f"Today's low: {daily['temperature_2m_min'][0]} °C")
print(
    f"Chance of rain: "
    f"{daily['precipitation_probability_max'][0]}%"
)
print(f"Wind speed: {current['wind_speed_10m']} km/h")
