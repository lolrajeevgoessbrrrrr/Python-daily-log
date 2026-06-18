import requests 
response = requests.get("https://official-joke-api.appspot.com/random_joke")
response.raise_for_status()  # Check for HTTP request errors
data = response.json()
try:
    print(type(data))
    print(data)
    print(data["setup"])
    print(data["punchline"])
    print(f"Joke: {data['setup']} - {data['punchline']}")
except requests.exceptions.ConnectionError as e:
    print(f"An connection error occurred: {e}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")