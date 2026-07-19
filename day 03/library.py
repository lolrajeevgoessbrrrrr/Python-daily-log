import requests
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
data = response.json()

print("Title:", data["title"])
print("Body:", data["body"])
print("Post ID:", data["userId"])

user_id = int(input("\nEnter a post number (1-10): "))
response2 = requests.get(f"https://jsonplaceholder.typicode.com/posts/{user_id}")
data2 = response2.json()
print("\nYou picked:", data2["title"])