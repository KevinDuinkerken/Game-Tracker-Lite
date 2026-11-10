import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "profiles_and_games.json"


def load_profiles():
    """Laadt alle profielen en hun opgeslagen games uit het JSON-bestand."""

    try:
        with open(DATA_FILE, "r") as file:
            saved_profiles = json.load(file)
        return saved_profiles

    except FileNotFoundError:
        return {}


def save_profiles(saved_profiles):
    """Slaat alle profielen en hun games op in het JSON-bestand."""

    with open(DATA_FILE, "w") as file:
        json.dump(saved_profiles, file)


def load_profile_games(profile_name):
    """Haalt de opgeslagen games van een specifiek profiel op."""

    saved_profiles = load_profiles()

    if profile_name in saved_profiles:
        return saved_profiles[profile_name]

    else:
        return None


def save_profile_games(profile_name, saved_games):
    """Slaat de bijgewerkte gamelijst van een specifiek profiel op."""

    saved_profiles = load_profiles()
    saved_profiles[profile_name] = saved_games

    save_profiles(saved_profiles)
