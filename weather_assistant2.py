
import requests
import ollama

while True:
    place = input("\nEnter a city or area (or type 'exit'): ")

    if place.lower() == "exit":
        print("Weather assistant closed.")
        break

    try:
        # Step 1: Convert place name into coordinates
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": place,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url, params=geo_params, timeout=10
        )
        geo_response.raise_for_status()

        locations = geo_response.json().get("results", [])

        if not locations:
            print("Location not found. Try another place.")
            continue

        location = locations[0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        city = location["name"]
        country = location.get("country", "")

        # Step 2: Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "wind_speed_10m"
            ],
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url, params=weather_params, timeout=10
        )
        weather_response.raise_for_status()

        weather = weather_response.json()["current"]

        # Step 3: Send actual weather data to the local LLM
        prompt = f"""
        You are a friendly weather assistant.
        Explain the current weather in {city}, {country}
        in simple English.

        Temperature: {weather['temperature_2m']} °C
        Feels like: {weather['apparent_temperature']} °C
        Humidity: {weather['relative_humidity_2m']}%
        Wind speed: {weather['wind_speed_10m']} km/h

        Explain whether it feels hot or comfortable.
        Give one useful suggestion.
        Use only the data provided.
        Do not invent weather details.
        """

        answer = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        print(f"\nWeather report for {city}, {country}")
        print(answer.message.content)

    except requests.RequestException as error:
        print("Weather API error:", error)

    except Exception as error:
        print("Something went wrong:", error)
