
import requests
import ollama

# 1. Get live weather data from the API
url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 13.0827,
    "longitude": 80.2707,
    "current": [
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "wind_speed_10m"
    ],
    "timezone": "Asia/Kolkata"
}

response = requests.get(url, params=params, timeout=10)
response.raise_for_status()

weather = response.json()["current"]

print("Weather data received from API:", weather)

# 2. Send the weather data to the local LLM
prompt = f"""
You are a friendly weather assistant.
Explain today's current weather in Chennai in simple English.

Here is the actual weather data:
Temperature: {weather['temperature_2m']} °C
Feels like: {weather['apparent_temperature']} °C
Humidity: {weather['relative_humidity_2m']}%
Wind speed: {weather['wind_speed_10m']} km/h

Explain whether it feels hot or comfortable and give one useful suggestion.
Use only the data provided. Do not invent weather details.
"""

answer = ollama.chat(
    model="llama3.2:1b",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# 3. Display the LLM's answer
print("\nWeather Assistant:")
print(answer.message.content)
