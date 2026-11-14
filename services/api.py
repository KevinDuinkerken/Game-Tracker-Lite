import requests
from services import logger


BASE_URL = "https://www.freetogame.com/api/"


def get_games_by_category(category_choice):
    """Haalt games op uit de FreeToGame API op basis van de gekozen categorie."""

    try:
        response = requests.get(f"{BASE_URL}games?category={category_choice.lower()}", timeout=10)
        response.raise_for_status()
        games = response.json()
        return games
    except requests.exceptions.RequestException as error:
        print("\nEr is iets misgegaan met het ophalen van games.")
        logger.log_error(str(error))
        return None


def get_game_details(game_id):
    """Haalt details op over een game via de FreeToGame API."""

    try:
        response = requests.get(f"{BASE_URL}game?id={game_id}", timeout=10)
        response.raise_for_status()
        game_details = response.json()
        return game_details
    except requests.exceptions.RequestException as error:
        print("\nEr is iets misgegaan met het ophalen van games.")
        logger.log_error(str(error))
        return None
