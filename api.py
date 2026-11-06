import requests

BASE_URL = "https://www.freetogame.com/api/"


def get_games_by_category(category_choice):
    response = requests.get(f"{BASE_URL}games?category={category_choice.lower()}")
    games = response.json()
    return games


def get_game_details(game_id):
    response = requests.get(f"{BASE_URL}game?id={game_id}")
    game_details = response.json()
    return game_details
