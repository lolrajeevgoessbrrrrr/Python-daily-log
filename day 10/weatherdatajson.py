weather_data = {
    "city": "Lucknow",
    "main": {
        "temp": 38,
        "humidity": 45
    },
    "weather": [
        {"description": "clear sky"},
        {"description": "hot"}
    ],
    "wind": {
        "speed": 12
    }
}

print(weather_data["main"]["temp"])
print(weather_data["weather"][0]["description"])
print(weather_data["wind"]["speed"])