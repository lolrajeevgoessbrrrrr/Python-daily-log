import requests
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OWM_API_KEY")  # Get the API key from environment variables
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        
        print(f"\nWeather in {city}:")
        print(f"Temperature : {temp}°C (feels like {feels_like}°C)")
        print(f"Condition   : {description}")
        print(f"Humidity    : {humidity}%")
        
    except requests.exceptions.HTTPError:
        print("City not found. Check the spelling.")
    except requests.exceptions.ConnectionError:
        print("No internet connection.")

city = input("Enter a city name to get the current weather: ")
get_weather(city)