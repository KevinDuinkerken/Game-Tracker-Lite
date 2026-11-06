import api
import storage
import profiles


CATEGORIES = {
    "1": "MMORPG",
    "2": "Shooter",
    "3": "Strategy",
    "4": "Racing",
    "5": "Sports",
    "6": "Battle-Royale",
}


def check_saved_games(selected_profile):
    print("\n***** OPGESLAGEN GAMES *****")

    saved_games = storage.load_profile_games(selected_profile)

    if not saved_games:
        print("Je hebt nog geen games opgeslagen.")
        return

    for number, game in enumerate(saved_games, start=1):
        print(f"{number}: {game['title']} - {game['status']}")


def show_status_menu():
    print("***** KIES NIEUWE SPEELSTATUS *****")
    print("1: Wil ik spelen")
    print("2: Aan het spelen")
    print("3: Uitgespeeld")
    print("0: Annuleren")


def change_game_status(selected_profile):
    print("\n***** SPEELSTATUS WIJZIGEN *****")

    saved_games = storage.load_profile_games(selected_profile)

    if not saved_games:
        print("Je hebt nog geen games opgeslagen.")
        return

    for number, game in enumerate(saved_games, start=1):
        print(f"{number}: {game['title']}")

    print("0: Terug naar gamelijstmenu\n")

    try:
        game_choice = int(input("Welke game wil je wijzigen? ").strip())

    except ValueError:
        print("Voer een geldig gamenummer in.")
        return

    if game_choice == 0:
        return

    elif 1 <= game_choice <= len(saved_games):
        selected_game = saved_games[game_choice - 1]
        print(f"Geselecteerde game: {selected_game['title']}\nHuidige speelstatus: {selected_game['status']}\n")
        show_status_menu()

        status_choice = input("Maak een keuze: ").strip()

        if status_choice == "0":
            return

        elif status_choice == "1":
            selected_game["status"] = "Wil ik spelen"

        elif status_choice == "2":
            selected_game["status"] = "Aan het spelen"

        elif status_choice == "3":
            selected_game["status"] = "Uitgespeeld"

        else:
            print("Ongeldige keuze, probeer opnieuw.")
            return

        storage.save_profile_games(selected_profile, saved_games)

        print(f"\nSpeelstatus succesvol gewijzigd naar: {selected_game['status']}")

    else:
        print("Ongeldige keuze, probeer opnieuw.")


def remove_game(selected_profile):
    print("\n***** GAME VERWIJDEREN *****")

    saved_games = storage.load_profile_games(selected_profile)

    if not saved_games:
        print("Je hebt nog geen games opgeslagen.")
        return

    for number, game in enumerate(saved_games, start=1):
        print(f"{number}: {game['title']}")

    print("0: Terug naar gamelijstmenu\n")

    try:
        game_choice = int(input("Welke game wil je verwijderen? ").strip())

    except ValueError:
        print("Voer een geldig gamenummer in.")
        return

    if game_choice == 0:
        return

    elif 1 <= game_choice <= len(saved_games):
        selected_game = saved_games[game_choice - 1]
        confirmation = input(f"Weet je zeker dat je {selected_game['title']} wilt verwijderen? (ja/nee): ").strip().lower()

        if confirmation == "ja":
            saved_games.pop(game_choice - 1)
            storage.save_profile_games(selected_profile, saved_games)
            print(f"{selected_game['title']} is succesvol verwijderd uit je gamelijst.")

        elif confirmation == "nee":
            print("Verwijderen geannuleerd.")
            return

        else:
            print("Ongeldige invoer, antwoord met ja of nee.")

    else:
        print("Ongeldige keuze, probeer opnieuw.")


def handle_game_details_menu(selected_game, selected_profile):
    while True:
        choice = show_game_details_menu()

        if choice == "1":
            add_game(selected_game, selected_profile)
            return

        elif choice == "0":
            return

        else:
            print("Ongeldige keuze, probeer opnieuw.")


def show_game_details_menu():
    print("\n***** GAME OPTIES *****")
    print("1: Toevoegen aan mijn gamelijst")
    print("0: Terug naar categorieën\n")

    return input("Maak een keuze: ").strip()


def add_game(selected_game, selected_profile):
    saved_games = storage.load_profile_games(selected_profile)

    for game in saved_games:
        if game["id"] == selected_game["id"]:
            print(f"{selected_game['title']} staat al in je gamelijst.")
            return

    saved_game = {
        "id": selected_game["id"],
        "title": selected_game["title"],
        "status": "Wil ik spelen"
    }

    saved_games.append(saved_game)
    storage.save_profile_games(selected_profile, saved_games)
    print(f"{selected_game['title']} is succesvol toegevoegd aan je gamelijst.")


def show_game_details(game_details):
    print("\n***** GAME DETAILS *****")
    print(f"Titel: {game_details['title']}")
    print(f"Genre: {game_details['genre']}")
    print(f"Platform: {game_details['platform']}")
    print(f"Beschrijving: {game_details['description']}")


def select_game(games, selected_profile):
    while True:
        try:
            game_choice = int(input("Welke game wil je bekijken? ").strip())

        except ValueError:
            print("Ongeldige invoer, voer een getal in.")
            continue

        if game_choice == 0:
            return

        elif 1 <= game_choice <= len(games):
            selected_game = games[game_choice - 1]
            game_id = selected_game["id"]
            game_details = api.get_game_details(game_id)
            show_game_details(game_details)
            handle_game_details_menu(selected_game, selected_profile)
            return

        else:
            print("\nOngeldige keuze, probeer opnieuw.")


def show_games(games):
    print("\n***** GEVONDEN GAMES *****")

    for number, game in enumerate(games, start=1):
        print(f"{number}: {game['title']}")

    print("0: Terug naar categorieën\n")


def handle_game_list_menu(selected_profile):
    while True:
        choice = show_game_list_menu()

        if choice == "0":
            return

        elif choice == "1":
            check_saved_games(selected_profile)

        elif choice == "2":
            change_game_status(selected_profile)

        elif choice == "3":
            remove_game(selected_profile)

        else:
            print("\nOngeldige keuze, probeer opnieuw.")


def handle_search_menu(selected_profile):
    while True:
        choice = show_search_menu()

        if choice == "0":
            return

        elif choice in CATEGORIES:
            category_choice = CATEGORIES[choice]
            print(f"\nJe hebt {category_choice} gekozen.")
            games = api.get_games_by_category(category_choice)
            show_games(games)
            select_game(games, selected_profile)

        else:
            print("\nOngeldige keuze, probeer opnieuw.")


def show_game_list_menu():
    print("\n***** MIJN GAMELIJST BEHEREN *****")
    print("1: Opgeslagen games bekijken")
    print("2: Speelstatus wijzigen")
    print("3: Game verwijderen")
    print("0: Terug naar hoofdmenu\n")

    return input("Maak een keuze: ").strip()


def show_search_menu():
    print("\n***** GAMES ZOEKEN OP CATEGORIE *****")

    for number, category in CATEGORIES.items():
        print(f"{number}: {category}")

    print("0: Terug naar hoofdmenu\n")

    return input("Welke categorie zou je graag willen zoeken? ").strip()


def show_main_menu(selected_profile):
    print("\n***** HOOFDMENU *****")

    if selected_profile:
        print(f"Actief profiel: {selected_profile}\n")

    else:
        print("Geen profiel geselecteerd. Maak een profiel aan of kies een bestaand profiel.\n")

    print("1: Games zoeken op categorie")
    print("2: Mijn gamelijst beheren")
    print("3: Profielen beheren")
    print("0: Applicatie afsluiten\n")

    return input("Maak een keuze: ").strip()


def main():
    selected_profile = profiles.start_with_profile()

    while True:
        choice = show_main_menu(selected_profile)

        if choice == "0":
            print("\nGame Tracker Lite wordt afgesloten, tot de volgende keer!")
            break

        elif choice == "1":
            handle_search_menu(selected_profile)

        elif choice == "2":
            handle_game_list_menu(selected_profile)

        elif choice == "3":
            profile_result = profiles.handle_profile_menu()

            if profile_result:
                action, profile_name = profile_result

                if action == "selected":
                    selected_profile = profile_name

                elif action == "deleted" and profile_name == selected_profile:
                    selected_profile = profiles.start_with_profile()

        else:
            print("Ongeldige keuze, probeer opnieuw.")


if __name__ == "__main__":
    main()
