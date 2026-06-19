import requests

response = requests.get(
    "https://official-joke-api.appspot.com/random_joke"
)

if response.status_code == 200:
    joke = response.json()

    print("Setup:")
    print(joke["setup"])

    print("\nPunchline:")
    print(joke["punchline"])
else:
    print("Error getting joke")