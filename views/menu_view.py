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

    @staticmethod
    def validate_id_view():
        title = "Veuillez choisir un ID parmi les suivants :  "
        options = [
            "Admin",
            "Support",
            "Sales"
        ]
        return title, options

    def display_menu(self, menu_options, action_map):
        title, options = menu_options
        choice = self.select_choice(title, options)
        action_map[choice]()

    @staticmethod
    def validate_existing_user_id_view():
        MenuView.console.print("[bold red]ID d'utilisateur non valide.[/bold red]")

    @staticmethod
    def validate_existing_contract_id_view():
        MenuView.console.print("[bold red]ID de contrat non valide.[/bold red]")

    @staticmethod
    def validate_existing_customer_id_view():
        MenuView.console.print("[bold red]ID de client non valide.[/bold red]")

    @staticmethod
    def validate_existing_event_id_view():
        MenuView.console.print("[bold red]ID d'événement non trouvé.[/bold red]")

    @staticmethod
    def validate_add_support_to_event_view():
        MenuView.console.print("[bold red]Utilisateur non trouvé ou n'est pas un support.[/bold red]")

    @staticmethod
    def validate_eight_ch_password_view():
        MenuView.console.print("[bold red]Le mot de passe doit contenir au moins 8 caractères.[/bold red]")

    @staticmethod
    def validate_maj_password_view():
        MenuView.console.print("[bold red]Le mot de passe doit contenir une lettre majuscule.[/bold red]")

    @staticmethod
    def validate_min_password_view():
        MenuView.console.print("[bold red]Le mot de passe doit contenir une lettre minuscule[/bold red]")

    @staticmethod
    def validate_num_password_view():
        MenuView.console.print("[bold red]Le mot de passe doit contenir un chiffre[/bold red]")

    @staticmethod
    def validate_str_view():
        MenuView.console.print("[bold red]Chaîne de caractères non valide.[/bold red]")

    @staticmethod
    def validate_email_view():
        MenuView.console.print("[bold red]Email non valide.[/bold red]")

    @staticmethod
    def validate_phone_view():
        MenuView.console.print("[bold red]Numéro de téléphone non valide.[/bold red]")

    @staticmethod
    def validate_attendees_view():
        MenuView.console.print("[bold red]Nombre de participants non valide.[/bold red]")

    @staticmethod
    def validate_amount_total_view():
        MenuView.console.print("[bold red]Montant total non valide.[/bold red]")

    @staticmethod
    def validate_amount_due_view():
        MenuView.console.print("[bold red]Montant dû non valide.[/bold red]")

    @staticmethod
    def validate_boolean_view():
        MenuView.console.print("[bold red]Merci de choisir parmi 'True' ou 'False'.[/bold red]")

    @staticmethod
    def store_tokens_view(user_id):
        MenuView.console.print(f"[bold green]Tokens enregistrés pour l'utilisateur {user_id}.[/bold green]")

    @staticmethod
    def get_tokens_view(user_id):
        MenuView.console.print(f"[bold blue]Tokens récupérés pour l'utilisateur {user_id}.[/bold blue]")

    @staticmethod
    def clear_cache_view(user_id):
        MenuView.console.print(f"[bold green]Cache vidé pour l'utilisateur {user_id}.[/bold green]")

    @staticmethod
    def refresh_tokens_view():
        MenuView.console.print("[bold red]Erreur lors de l'actualisation des tokens[/bold red]")

    @staticmethod
    def check_token_view():
        MenuView.console.print("[bold red]Token invalide ou expiré.[/bold red]")

    @staticmethod
    def required_token_view():
        MenuView.console.print("[bold red]Tokens requis.[/bold red]")

    @staticmethod
    def missing_token_view():
        MenuView.console.print("[bold red]Tokens manquants.[/bold red]")

    @staticmethod
    def invalid_token_view():
        MenuView.console.print("[bold red]Token invalide ou expiré.[/bold red]")
