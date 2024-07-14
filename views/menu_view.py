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
            "Afficher les utilisateurs",
            "Afficher les clients",
            "Afficher les contrats",
            "Afficher les événements",
            "Quitter l'app"
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
        options = ["Afficher les evenements",
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
            "Supprimer un contrat",
            "Filtrer les évenements",
            "Assigner un évenement à un support",
            "Database [Read Only]",
            "Se déconnecter"
        ]
        return title, options

    @staticmethod
    def filtered_contact_menu_options():
        title = "Contacts filter"
        options = [
            "Contrats non signés",
            "Contrats impayés",
            "Contrats signés",
            "Tous les contrats"
        ]
        return title, options

    @staticmethod
    def filtered_event_menu_options():
        title = "Filtrer les événements"
        options = [
            "Événements sans support",
            "Événements à venir",
            "Événements passés",
            "Tous les événements"
        ]
        return title, options

    def display_menu(self, menu_options, action_map):
        title, options = menu_options
        choice = self.select_choice(title, options)
        action_map[choice]()
