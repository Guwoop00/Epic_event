from rich.console import Console


class UserView:
    console = Console()

    def input_login_view(self):
        self.console.print("\n[bold yellow]Entrer vos identifiants[/bold yellow]\n")
        username = input("Email de connection: ")
        password = input("Mot de passe: ")
        return username, password

    def get_create_user_prompts(self):
        self.console.print("\n[bold yellow]Créer un nouvel utilisateur[/bold yellow]\n")
        prompts = {
            "full_name": "Nom complet: ",
            "email": "Email: ",
            "password": "Mot de passe: ",
            "role_id": "Rôle ID (1: admin, 2: support, 3: sales): "
        }
        return prompts

    def get_update_user_prompts(self):
        self.console.print("\n[bold yellow]Mettre à jour l'utilisateur[/bold yellow]\n")
        prompts = {
            "full_name": "Nom complet (laisser vide pour ne pas changer): ",
            "email": "Email (laisser vide pour ne pas changer): ",
            "password": "Mot de passe (laisser vide pour ne pas changer): ",
            "role_id": "Rôle ID (1: admin, 2: support, 3: sales) (laisser vide pour ne pas changer): "
        }
        return prompts

    def user_view_prompts(self):
        prompts = {
            "user_id": "ID: "
        }
        return prompts

    @staticmethod
    def authenticated_user_view():
        UserView.console.print("\n[bold green]Connexion réussie ![/bold green]\n")

    @staticmethod
    def unauthenticated_user_view():
        UserView.console.print("\n[bold red]Utilisateur ou mot de passe incorrect ![/bold red]\n")

    @staticmethod
    def user_not_found():
        UserView.console.print("\n[bold red]Utilisateur non trouvé.[/bold red]\n")

    @staticmethod
    def incorrect_password():
        UserView.console.print("\n[bold red]Mot de passe incorrect.[/bold red]\n")

    @staticmethod
    def access_granted(token):
        UserView.console.print(f"\n[bold cornflower_blue]Token:[/bold cornflower_blue] {token}")

    @staticmethod
    def user_created():
        UserView.console.print("\n[bold green]Utilisateur créé avec succès.[/bold green]\n")

    @staticmethod
    def user_updated():
        UserView.console.print("\n[bold green]Utilisateur mis à jour avec succès.[/bold green]\n")

    @staticmethod
    def user_deleted():
        UserView.console.print("\n[bold green]Utilisateur supprimé avec succès.[/bold green]\n")

    @staticmethod
    def table_created_successfull():
        UserView.console.print("\n[bold green]Tables créées avec succès.[/bold green]\n")

    @staticmethod
    def table_creation_error(e):
        UserView.console.print(f"\n[bold red]Erreur lors de la création des tables : {e}[/bold red]\n")

    @staticmethod
    def role_created_successfull(role_name):
        UserView.console.print(f"\n[bold green]Rôle '{role_name}' créé avec succès.[/bold green]\n")

    @staticmethod
    def role_creation_error(e):
        UserView.console.print(f"\n[bold red]Erreur lors de la création des rôles : {e}[/bold red]\n")

    @staticmethod
    def admin_user_created_successfull():
        UserView.console.print("\n[bold green]Utilisateur admin créé avec succès.[/bold green]\n")

    @staticmethod
    def admin_user_created_error(e):
        UserView.console.print(f"\n[bold red]Erreur lors de la création de l'utilisateur admin : {e}[/bold red]\n")

    @staticmethod
    def prompt_change_password_view():
        UserView.console.print("\n[bold yellow]Veuillez entrer un nouveau mot de passe :[/bold yellow]\n")

    @staticmethod
    def password_updated_successfull():
        UserView.console.print("\n[bold green]Mot de passe mis à jour avec succès.[/bold green]\n")
