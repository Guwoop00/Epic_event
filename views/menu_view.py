from rich.console import Console
from rich.table import Table


class MenuView:
    console = Console()

    @classmethod
    def select_choice(cls, title, options):
        cls.console.print(f"\n[bold yellow underline]{title}[/bold yellow underline]\n")
        table = Table(show_header=True, header_style="bold cornflower_blue")
        table.add_column("Option", style="yellow", justify="center")
        table.add_column("Description", justify="center")

        for i, option in enumerate(options, start=1):
            table.add_row(str(i), option)

        cls.console.print(table)
        while True:
            try:
                choice = int(input("Quel est votre choix: "))
                if 1 <= choice <= len(options):
                    return choice
                else:
                    cls.console.print(f"\n[bold red]Choix invalide. "
                                      f"Merci d'entrer un nombre entre 1 et {len(options)}[/bold red]\n")
            except ValueError:
                cls.console.print("\n[bold red]Choix invalide. Merci de rentrer un nombre valide.[/bold red]\n")

    @classmethod
    def get_user_choice(cls):
        return int(input("\nQuel est votre choix ? : \n"))

    @staticmethod
    def input_error():
        console = Console()
        console.print("\n[bold red]Input error, entrez une option valide ![/bold red]\n")

    @staticmethod
    def login_menu_options():
        title = "Login"
        options = ["Se connecter",
                   "Quitter le programme"]
        return title, options

    @staticmethod
    def database_menu_options():
        title = "Base de données"
        options = [
            "Afficher les clients",
            "Afficher les contrats",
            "Afficher les événements",
            "Menu principal"
        ]
        return title, options

    @staticmethod
    def sales_menu_options():
        title = "Menu Commercial"
        options = ["Créer un client",
                   "Modifier un client",
                   "Créer un évenement",
                   "Modifier un contrat",
                   "Afficher les contrats",
                   "Database [Read Only]",
                   "Log out"]
        return title, options

    @staticmethod
    def support_menu_options():
        title = "Menu Support"
        options = ["Filtrer les evenements",
                   "Database [Read Only]",
                   "Log out"]
        return title, options

    @staticmethod
    def admin_menu_options():
        title = "Menu Administrateur"
        options = [
            "Créer un collaborateur",
            "Modifier un collaborateur",
            "Suprimer un collaborateur",
            "Créer un contrat",
            "Filtrer les évenements",
            "Assigner un support à un évenement",
            "Database [Read Only]",
            "Se déconnecter"
        ]
        return title, options

    @staticmethod
    def filtered_contracts_menu_options():
        title = "Contracts filter"
        options = [
            "Contrats non signés",
            "Contrats impayés",
            "Contrats signés",
            "Tous les contrats"
        ]
        return title, options

    @staticmethod
    def filtered_event_admin_menu_options():
        title = "Filtrer les événements"
        options = [
            "Événements sans support",
            "Événements à venir",
            "Événements passés",
            "Tous les événements"
        ]
        return title, options

    @staticmethod
    def filtered_event_support_menu_options():
        title = "Filtrer les événements"
        options = [
            "Mes événements",
            "Tous les événements"
        ]
        return title, options

    def display_menu(self, menu_options, action_map):
        title, options = menu_options
        choice = self.select_choice(title, options)
        action_map[choice]()

    @staticmethod
    def contract_not_assigned_to_user(contract_id, user_id):
        MenuView.console.print(
            f"\n[bold red]Erreur:[/bold red] Le contrat ID {contract_id}"
            f"n'est pas assigné à l'utilisateur ID {user_id}.\n"
        )

    @staticmethod
    def validate_role_id_view(role_id):
        MenuView.console.print(
            f"\n[bold red]Erreur:[/bold red] Aucun role trouvé avec cet ID {role_id}.\n"
        )

    @staticmethod
    def contract_not_found(contract_id):
        MenuView.console.print(
            f"\n[bold red]Erreur:[/bold red] Aucun contrat trouvé avec l'ID {contract_id}.\n"
        )

    @staticmethod
    def customer_not_assigned_to_user(customer_id, user_id):
        MenuView.console.print(
            f"\n[bold red]Erreur:[/bold red] Le client ID {customer_id}"
            f"n'est pas assigné à l'utilisateur ID {user_id}.\n"
        )

    @staticmethod
    def customer_not_found(customer_id):
        MenuView.console.print(
            f"\n[bold red]Erreur:[/bold red] Aucun client trouvé avec l'ID {customer_id}.\n"
        )

    @staticmethod
    def event_not_found(event_id):
        MenuView.console.print(
            f"\n[bold red]Erreur:[/bold red] Aucun événement trouvé avec l'ID {event_id}.\n"
        )

    @staticmethod
    def user_not_support(user_id):
        MenuView.console.print(
            f"\n[bold red]Erreur:[/bold red] L'utilisateur ID {user_id} n'est pas un membre du support.\n"
        )

    @staticmethod
    def user_not_found(user_id):
        MenuView.console.print(
            f"\n[bold red]Erreur:[/bold red] Aucun utilisateur trouvé avec l'ID {user_id}.\n"
        )

    @staticmethod
    def password_too_short():
        MenuView.console.print(
            "\n[bold red]Erreur:[/bold red] Le mot de passe doit comporter au moins 8 caractères.\n"
        )

    @staticmethod
    def password_missing_uppercase():
        MenuView.console.print(
            "\n[bold red]Erreur:[/bold red] Le mot de passe doit contenir au moins une lettre majuscule.\n"
        )

    @staticmethod
    def password_missing_lowercase():
        MenuView.console.print(
            "\n[bold red]Erreur:[/bold red] Le mot de passe doit contenir au moins une lettre minuscule.\n"
        )

    @staticmethod
    def password_missing_number():
        MenuView.console.print(
            "\n[bold red]Erreur:[/bold red] Le mot de passe doit contenir au moins un chiffre.\n"
        )

    @staticmethod
    def invalid_string():
        MenuView.console.print(
            "\n[bold red]Erreur:[/bold red]Erreur:[/bold red] La chaîne de caractères saisie n'est pas valide.\n"
        )

    @staticmethod
    def user_role_error():
        MenuView.console.print(
            "[bold red]Erreur:[/bold red] Cet utilisateur est un admin."
        )

    @staticmethod
    def user_not_found_error():
        MenuView.console.print(
            "[bold red]Erreur:[/bold red] Cet utilisateur n'existe pas."
        )

    @staticmethod
    def validate_email_view():
        MenuView.console.print(
            "[bold red]Erreur:[/bold red] Email non valide."
        )

    @staticmethod
    def validate_phone_view():
        MenuView.console.print(
            "[bold red]Erreur:[/bold red ]Numéro de téléphone non valide."
        )

    @staticmethod
    def validate_attendees_view():
        MenuView.console.print(
            "[bold red]Erreur:[/bold red] Nombre de participants non valide."
        )

    @staticmethod
    def validate_amount_total_view():
        MenuView.console.print(
            "[bold red]Erreur:[/bold red] Montant total non valide."
        )

    @staticmethod
    def validate_amount_due_view():
        MenuView.console.print(
            "[bold red]Erreur:[/bold red] Montant dû non valide."
        )

    @staticmethod
    def validate_boolean_view():
        MenuView.console.print(
            "[bold red]Erreur:[/bold red] Merci de choisir parmi 'True' ou 'False'."
        )

    @staticmethod
    def store_tokens_view(user_id):
        MenuView.console.print(
            f"[bold green]Tokens enregistrés pour l'utilisateur {user_id}.[/bold green]"
        )

    @staticmethod
    def get_tokens_view(user_id):
        MenuView.console.print(
            f"[bold blue]Tokens récupérés pour l'utilisateur {user_id}.[/bold blue]"
        )

    @staticmethod
    def clear_cache_view(user_id):
        MenuView.console.print(
            f"[bold green]Cache vidé pour l'utilisateur {user_id}.[/bold green]"
        )

    @staticmethod
    def check_token_view():
        MenuView.console.print(
            "[bold red]Token invalide ou expiré.[/bold red]"
        )

    @staticmethod
    def required_token_view():
        MenuView.console.print(
            "[bold red]Erreur:[/bold red] Tokens requis."
        )

    @staticmethod
    def missing_token_view():
        MenuView.console.print(
            "[bold red]Erreur:[/bold red] Tokens manquants."
        )

    @staticmethod
    def invalid_token_view():
        MenuView.console.print(
            "[bold red]Erreur:[/bold red] Token invalide ou expiré.[/bold red]"
        )
