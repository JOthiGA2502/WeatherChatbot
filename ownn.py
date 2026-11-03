
import requests
import ollama

try:
    c_name=input("enter the city name:")
    url1="https://geocoding-api.open-meteo.com/v1/search"
    params={
        "name":c_name,
        "count":1,
        "format":"json",
        "language":"en"
    }
    responce=requests.get(url1, params=params, timeout=10)
    responce.raise_for_status()
    data=responce.json()
    dict=data.get("results",[])
    if not dict:
        print("location not found ,try another place")
    else:
        latitude=dict[0]["latitude"]
        longitude=dict[0]["longitude"]



    url2="https://api.open-meteo.com/v1/forecast"
    params2={
        "latitude":latitude,
        "longitude":longitude,
        "current":["temperature_2m","relative_humidity_2m","apparent_temperature","wind_speed_10m"],
        "timezone":"auto"
    }
    responce2=requests.get(url2,params=params2,timeout=10)
    data2=responce2.json()
    temperature=data2["current"]["temperature_2m"]
    humidity=data2["current"]["relative_humidity_2m"]
    wind_speed=data2["current"]["wind_speed_10m"]

    prompt=f"""
    i will provie you a city name and data about the weather condition of that city 
    you give content like a weather reporter based on the data and give some suggestions to be healthy based on the weather 

    city={c_name} , temperature={data2["current"]["temperature_2m"]}
    humidity={data2["current"]["relative_humidity_2m"]}
    wind_speed={data2["current"]["wind_speed_10m"]}
    """

    ai=ollama.chat(
        model="llama3.2:1b",
        messages=[
        {"role":"user" , "content":prompt}
        ]
        
    )
    print(ai["message"]["content"])

except requests.Exceptions.Timeout as e:
    print(e)

except requests.Exceptions.ConnectionError as e:
    print(e)

except requests.Exceptions.HTTPError as e:
    print(e)
    