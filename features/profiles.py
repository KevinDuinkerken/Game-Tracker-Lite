from services import storage, logger


def create_profile():
    """Maakt een nieuw profiel aan."""

    profile_name = input("Voer een nieuwe profielnaam in: ").strip().capitalize()

    if not profile_name:
        print("Je hebt niks ingevuld.")
        return None

    saved_profiles = storage.load_profiles()

    if profile_name in saved_profiles:
        print("Dit profiel bestaat al.")
        return None

    saved_profiles[profile_name] = []

    storage.save_profiles(saved_profiles)

    print(f"Profiel {profile_name} is succesvol aangemaakt.")

    return profile_name


def show_profiles(saved_profiles):
    """Toont een genummerd overzicht van de bestaande profielen."""

    if not saved_profiles:
        print("Er zijn nog geen profielen aangemaakt.")
        return

    print("\n***** BESCHIKBARE PROFIELEN *****")

    for number, profile_name in enumerate(saved_profiles, start=1):
        print(f"{number}: {profile_name}")


def show_profile_menu():
    """Toont het profielmenu en vraagt de gebruiker om een keuze."""

    print("\n***** PROFIELMENU *****")
    print("1: Profiel aanmaken")
    print("2: Profiel kiezen / wisselen")
    print("3: Profiel verwijderen")
    print("0: Terug naar hoofdmenu\n")

    return input("Maak een keuze: ").strip()


def handle_profile_menu():
    """Verwerkt de menukeuzes voor het aanmaken, selecteren en verwijderen van profielen."""

    while True:
        choice = show_profile_menu()

        if choice == "0":
            return None

        elif choice == "1":
            create_profile()

        elif choice == "2":
            selected_profile = select_profile()

            if selected_profile:
                return "selected", selected_profile

        elif choice == "3":
            deleted_profile = delete_profile()

            if deleted_profile:
                return "deleted", deleted_profile

        else:
            print("Ongeldige keuze, probeer opnieuw.")


def select_profile():
    """Laat de gebruiker een bestaand profiel selecteren."""

    saved_profiles = storage.load_profiles()

    show_profiles(saved_profiles)

    if not saved_profiles:
        return None

    print("0: Annuleren")

    try:
        profile_choice = int(input("Welk profiel wil je kiezen? ").strip())

    except ValueError as error:
        print("Voer een geldig profielnummer in.")
        logger.log_error(f"select_profile: {error}")
        return None

    if profile_choice == 0:
        return None

    elif 1 <= profile_choice <= len(saved_profiles):
        profile_names = list(saved_profiles)
        selected_profile = profile_names[profile_choice - 1]

        print(f"Hallo {selected_profile}")

        return selected_profile

    else:
        print("Ongeldige keuze, probeer opnieuw.")
        return None


def delete_profile():
    """Laat de gebruiker een profiel kiezen om te verwijderen."""

    saved_profiles = storage.load_profiles()

    if not saved_profiles:
        print("Er zijn geen profielen om te verwijderen.")
        return None

    show_profiles(saved_profiles)

    print("0: Annuleren")

    try:
        profile_choice = int(input("Welk profiel wil je verwijderen? ").strip())

    except ValueError as error:
        print("Voer een geldig profielnummer in.")
        logger.log_error(f"delete_profile: {error}")
        return None

    if profile_choice == 0:
        return None

    elif 1 <= profile_choice <= len(saved_profiles):
        profile_names = list(saved_profiles)
        selected_profile = profile_names[profile_choice - 1]

        confirmation = input(f"Weet je zeker dat je profiel {selected_profile} wilt verwijderen? (ja/nee): ").strip().lower()

        if confirmation == "ja":
            del saved_profiles[selected_profile]
            storage.save_profiles(saved_profiles)

            print(f"Profiel {selected_profile} is succesvol verwijderd.")

            return selected_profile

        elif confirmation == "nee":
            print("Profiel verwijderen geannuleerd.")
            return None

        else:
            print("Ongeldige keuze, probeer opnieuw.")
            return None

    else:
        print("Ongeldig profielnummer, probeer opnieuw.")
        return None


def start_with_profile():
    """Zorgt dat de gebruiker bij het opstarten een profiel aanmaakt of selecteert."""

    while True:
        saved_profiles = storage.load_profiles()

        if not saved_profiles:
            print("\nEr zijn nog geen profielen.")
            print("Maak eerst een profiel aan.\n")

            new_profile = create_profile()

            if new_profile:
                return new_profile

        else:
            print("\n***** INLOGGEN *****")


            show_profiles(saved_profiles)
            print("0: Nieuw profiel aanmaken\n")

            try:
                profile_choice = int(input("Welk profiel wil je gebruiken? ").strip())

            except ValueError as error:
                print("Voer een geldig profielnummer in.")
                logger.log_error(f"start_with_profile: {error}")
                continue

            if profile_choice == 0:
                new_profile = create_profile()

                if new_profile:
                    return new_profile

            elif 1 <= profile_choice <= len(saved_profiles):
                profile_names = list(saved_profiles)
                selected_profile = profile_names[profile_choice - 1]
                print(f"Hallo {selected_profile}")
                return selected_profile

            else:
                print("Ongeldige keuze, probeer opnieuw.")
