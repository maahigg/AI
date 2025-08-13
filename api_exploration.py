import requests

url = "https://official-joke-api.appspot.com/random_joke"

response = requests.get(url)

if response.status_code == 200:
    joke_data = response.json()
    print(f"joke : {joke_data['setup']} - {joke_data['punchline']}")
else:
    print(f"failed to retrieve code, status code: {response.status_code}")