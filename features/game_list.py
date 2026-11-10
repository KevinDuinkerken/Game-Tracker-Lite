from services import storage, logger


def show_game_list_menu():
    print("\n***** MIJN GAMELIJST BEHEREN *****")
    print("1: Opgeslagen games bekijken")
    print("2: Speelstatus wijzigen")
    print("3: Game verwijderen")
    print("0: Terug naar hoofdmenu\n")

    return input("Maak een keuze: ").strip()


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

    except ValueError as error:
        print("Voer een geldig gamenummer in.")
        logger.log_error(f"change_game_status: {error}")
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

    except ValueError as error:
        print("Voer een geldig gamenummer in.")
        logger.log_error(f"remove_game: {error}")
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
