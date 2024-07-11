class MenuView:

    def login_input(self):
        print("Entrer vos identifiants")
        email = input("Email de connexion: ")
        password = input("Mot de passe: ")
        return email, password

    @classmethod
    def select_choice(cls, title, options):
        print()
        print(title)
        print("********************")
        for i, option in enumerate(options, start=1):
            print(f"[{i}] {option}")
        print("********************")

        while True:
            try:
                choice = int(input("Quel est votre choix: "))
                if 1 <= choice <= len(options):
                    return choice
                else:
                    print("Choix invalide. Merci d'entrer un nombre entre 1 et", len(options))
            except ValueError:
                print("Choix invalide. Merci de rentrer un nombre valide.")

            return cls.get_user_choice()

    @classmethod
    def get_user_choice(cls):
        return int(input("Quel est votre choix ? : "))

    @staticmethod
    def input_error():
        print("Input error, entrez une option valide ! ")

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

    def display_menu(self, menu_options, action_map):
        title, options = menu_options
        choice = self.select_choice(title, options)
        action_map[choice]()
