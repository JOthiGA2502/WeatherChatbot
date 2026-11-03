
import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 13.0827,
    "longitude": 80.2707,
    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
    "timezone": "Asia/Kolkata"
}

response = requests.get(url, params=params, timeout=15)

print("Status code:", response.status_code)

data = response.json()
print(data["current"])
