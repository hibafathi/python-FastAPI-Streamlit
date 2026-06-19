import requests
from typing import Optional

GITHUB_URL = "https://api.github.com/users"
JOKE_URL = "https://official-joke-api.appspot.com/random_joke"


def fetch_user(username: str) -> Optional[dict]:
    try:
        response = requests.get(f"{GITHUB_URL}/{username}", timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"User '{username}' not found on GitHub")
            return None
        elif response.status_code == 403:
            print("GitHub API rate limit exceeded")
            return None
        else:
            print(f"GitHub API error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("No internet connection")
        return None
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Unexpected error: {e}")
        return None


def fetch_joke() -> Optional[tuple[str, str]]:
    try:
        response = requests.get(JOKE_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["setup"], data["punchline"]
        else:
            print(f"Joke API error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("No internet connection")
        return None
    except requests.exceptions.Timeout:
        print("Joke API timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Unexpected error: {e}")
        return None


def display_user(user: dict) -> None:
    joined: str = user.get("created_at", "N/A")[:10]
    print("=" * 38)
    print("        GitHub User Card")
    print("=" * 38)
    print(f"Name         : {user.get('name', 'N/A')}")
    print(f"Username     : {user.get('login', 'N/A')}")
    print(f"Location     : {user.get('location', 'N/A')}")
    print(f"Public Repos : {user.get('public_repos', 0)}")
    print(f"Followers    : {user.get('followers', 0)}")
    print(f"Following    : {user.get('following', 0)}")
    print(f"Joined       : {joined}")
    print(f"Profile      : {user.get('html_url', 'N/A')}")
    print("=" * 38)


def main() -> None:
    print("API Explorer with Type Hints")
    print("-" * 38)
    username: str = input("Enter GitHub username: ").strip()
    if not username:
        print("Username cannot be empty")
    else:
        print(f"Searching for '{username}'...")
        user: Optional[dict] = fetch_user(username)
        if user:
            display_user(user)
        else:
            print("Could not load user data.")
    print("Fetching a random joke...")
    result: Optional[tuple[str, str]] = fetch_joke()
    if result:
        setup, punchline = result
        print(f"Setup     : {setup}")
        input("Press Enter for punchline...")
        print(f"Punchline : {punchline}")
    else:
        print("Could not load joke.")


main()