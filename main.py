from features import profiles, game_list, game_search


def show_main_menu(selected_profile):
    """Toont het hoofdmenu met het actieve profiel en vraagt om een keuze."""

    print("\n***** HOOFDMENU *****")
    print(f"Actief profiel: {selected_profile}\n")

    print("1: Games zoeken op categorie")
    print("2: Mijn gamelijst beheren")
    print("3: Profielen beheren")
    print("0: Applicatie afsluiten\n")

    return input("Maak een keuze: ").strip()


def main():
    """Start de applicatie en verwerkt de keuzes uit het hoofdmenu."""

    selected_profile = profiles.start_with_profile()

    while True:
        choice = show_main_menu(selected_profile)

        if choice == "0":
            print("\nGame Tracker Lite wordt afgesloten, tot de volgende keer!")
            break

        elif choice == "1":
            game_search.handle_search_menu(selected_profile)

        elif choice == "2":
            game_list.handle_game_list_menu(selected_profile)

        elif choice == "3":
            profile_result = profiles.handle_profile_menu()

            if profile_result:
                action, profile_name = profile_result

                if action == "selected":
                    selected_profile = profile_name

                elif action == "deleted" and profile_name == selected_profile:
                    selected_profile = profiles.start_with_profile()

        else:
            print("\nOngeldige keuze, probeer opnieuw.")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nGame Tracker Lite is afgesloten.")
