import json



def load_profiles():
    try:
        with open("profiles_and_games.json", "r") as file:
            saved_profiles = json.load(file)
        return saved_profiles

    except FileNotFoundError:
        return {}


def save_profiles(saved_profiles):
    with open("profiles_and_games.json", "w") as file:
        json.dump(saved_profiles, file)


def load_profile_games(profile_name):
    saved_profiles = load_profiles()

    if profile_name in saved_profiles:
        return saved_profiles[profile_name]

    else:
        return None


def save_profile_games(profile_name, saved_games):
    saved_profiles = load_profiles()
    saved_profiles[profile_name] = saved_games

    save_profiles(saved_profiles)
