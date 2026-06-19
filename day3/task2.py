import requests

response = requests.get("https://api.github.com/users/octocat")

print("Status Code:", response.status_code)

if response.status_code == 200:
    user = response.json()

    print("Name:", user["name"])
    print("Location:", user["location"])
    print("Public Repos:", user["public_repos"])
    print("Created At:", user["created_at"])
else:
    print("Failed to fetch data")