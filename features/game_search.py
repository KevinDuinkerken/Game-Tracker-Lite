from services import api, logger
from features import game_list


CATEGORIES = {
    "1": "MMORPG",
    "2": "Shooter",
    "3": "Strategy",
    "4": "Racing",
    "5": "Sports",
    "6": "Battle-Royale",
}


def show_search_menu():
    """Toont de beschikbare gamecategorieën en vraagt om een keuze."""

    print("\n***** GAMES ZOEKEN OP CATEGORIE *****")

    for number, category in CATEGORIES.items():
        print(f"{number}: {category}")

    print("0: Terug naar hoofdmenu\n")

    return input("Welke categorie zou je graag willen zoeken? ").strip()


def handle_search_menu(selected_profile):
    """Verwerkt de gekozen categorie en haalt de bijbehorende games op."""

    while True:
        choice = show_search_menu()

        if choice == "0":
            return

        elif choice in CATEGORIES:
            category_choice = CATEGORIES[choice]
            print(f"\nJe hebt {category_choice} gekozen.")
            games = api.get_games_by_category(category_choice)
            if games is None:
                continue
            show_games(games)
            select_game(games, selected_profile)

        else:
            print("\nOngeldige keuze, probeer opnieuw.")


def show_games(games):
    """Toont een genummerd overzicht van de gevonden games."""

    print("\n***** GEVONDEN GAMES *****")

    for number, game in enumerate(games, start=1):
        print(f"{number}: {game['title']}")

    print("0: Terug naar categorieën\n")


def select_game(games, selected_profile):
    """Laat de gebruiker een game kiezen en haalt de details ervan op."""

    while True:
        try:
            game_choice = int(input("Welke game wil je bekijken? ").strip())

        except ValueError as error:
            print("Ongeldige invoer, voer een getal in.")
            logger.log_error(f"select_game: {error}")
            continue

        if game_choice == 0:
            return

        elif 1 <= game_choice <= len(games):
            selected_game = games[game_choice - 1]
            game_id = selected_game["id"]
            game_details = api.get_game_details(game_id)
            if game_details is None:
                return
            show_game_details(game_details)
            handle_game_details_menu(selected_game, selected_profile)
            return

        else:
            print("\nOngeldige keuze, probeer opnieuw.")


def show_game_details(game_details):
    """Toont details over de geselecteerde game."""

    print("\n***** GAME DETAILS *****")
    print(f"Titel: {game_details['title']}")
    print(f"Genre: {game_details['genre']}")
    print(f"Platform: {game_details['platform']}")
    print(f"Beschrijving: {game_details['description']}")


def show_game_details_menu():
    """Toont de opties voor een geselecteerde game en vraagt om een keuze."""

    print("\n***** GAME OPTIES *****")
    print("1: Toevoegen aan mijn gamelijst")
    print("0: Terug naar categorieën\n")

    return input("Maak een keuze: ").strip()


def handle_game_details_menu(selected_game, selected_profile):
    """Verwerkt de keuze om een game toe te voegen of terug te gaan."""

    while True:
        choice = show_game_details_menu()

        if choice == "1":
            game_list.add_game(selected_game, selected_profile)
            return

        elif choice == "0":
            return

        else:
            print("Ongeldige keuze, probeer opnieuw.")
