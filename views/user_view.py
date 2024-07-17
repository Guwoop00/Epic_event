from rich.console import Console
from rich.table import Table


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

    def input_user_id(self):
        self.console.print("\n[bold yellow]Entrez l'ID de l'utilisateur:[/bold yellow]\n")
        user_id = int(input("ID: "))
        return user_id

    def display_users_view(self, users):
        table = Table(title="\n[bold yellow underline]Détails de l'utilisateur[/bold yellow underline]\n")

        table.add_column("ID de l'utilisateur", header_style="bold cornflower_blue")
        table.add_column("Nom complet", header_style="bold cornflower_blue")
        table.add_column("Email", header_style="bold cornflower_blue")
        table.add_column("Rôle", header_style="bold cornflower_blue")

        for user in users:
            table.add_row(
                str(user.id),
                user.full_name,
                user.email,
                user.role.name
            )

        self.console.print(table)

    def authenticated_user_view(self):
        self.console.print("\n[bold green]Connexion réussie ![/bold green]\n")

    def unauthenticated_user_view(self):
        self.console.print("\n[bold red]Utilisateur ou mot de passe incorrect ![/bold red]\n")

    def user_not_found(self):
        self.console.print("\n[bold red]Utilisateur non trouvé.[/bold red]\n")

    def incorrect_password(self):
        self.console.print("\n[bold red]Mot de passe incorrect.[/bold red]\n")

    def access_granted(self, token):
        self.console.print(f"\n[bold cornflower_blue]Token:[/bold cornflower_blue] {token}")

    def user_created(self):
        self.console.print("\n[bold green]Utilisateur créé avec succès.[/bold green]\n")

    def user_updated(self):
        self.console.print("\n[bold green]Utilisateur mis à jour avec succès.[/bold green]\n")

    def user_deleted(self):
        self.console.print("\n[bold green]Utilisateur supprimé avec succès.[/bold green]\n")
