import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

# Melbourne coordinates
LATITUDE = -37.8136
LONGITUDE = 144.9631
MELBOURNE_TZ = ZoneInfo("Australia/Melbourne")

now = datetime.now(MELBOURNE_TZ)

# GitHub schedules use UTC. The workflow checks both possible UTC times
# because Melbourne changes between daylight-saving time and standard time.
# Only the run that lands at 9:00 AM Melbourne time sends a message.
if os.getenv("GITHUB_EVENT_NAME") == "schedule" and now.hour != 9:
    print(f"Melbourne time is {now:%H:%M}; not 09:00, so this run will not send.")
    raise SystemExit(0)

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

title = f"墨尔本天气｜{now:%Y-%m-%d}"
message = (
    f"## 🌤 墨尔本今日天气\n\n"
    f"- 当前温度：{current['temperature_2m']} °C\n"
    f"- 体感温度：{current['apparent_temperature']} °C\n"
    f"- 今日最高：{daily['temperature_2m_max'][0]} °C\n"
    f"- 今日最低：{daily['temperature_2m_min'][0]} °C\n"
    f"- 降雨概率：{daily['precipitation_probability_max'][0]}%\n"
    f"- 风速：{current['wind_speed_10m']} km/h"
)

print(title)
print(message)

sendkey = os.getenv("SERVERCHAN_SENDKEY")
if not sendkey:
    print("SERVERCHAN_SENDKEY is not configured, so no WeChat message was sent.")
    raise SystemExit(0)

push_response = requests.post(
    f"https://sctapi.ftqq.com/{sendkey}.send",
    data={"title": title, "desp": message},
    timeout=15,
)
push_response.raise_for_status()
result = push_response.json()

if result.get("code") != 0:
    raise RuntimeError(f"ServerChan rejected the message: {result.get('message', result)}")

print("WeChat message sent successfully.")
