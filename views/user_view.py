from rich.console import Console
from rich.table import Table


class UserView:
    console = Console()

    def input_login_view(self):
        self.console.print("\n[bold yellow]Entrer vos identifiants[/bold yellow]\n")
        username = input("Email de connection: ")
        password = input("Mot de passe: ")
        return username, password

    def input_user_data(self):
        self.console.print("\n[bold yellow]Créer un nouvel utilisateur[/bold yellow]\n")
        full_name = input("Nom complet: ")
        email = input("Email: ")
        password = input("Mot de passe: ")
        role_id = input("Rôle ID (1: admin, 2: support, 3: sales): ")
        return full_name, email, password, role_id

    def input_update_user_data(self):
        self.console.print("\n[bold yellow]Mettre à jour l'utilisateur[/bold yellow]\n")
        full_name = input("Nom complet (laisser vide pour ne pas changer): ")
        email = input("Email (laisser vide pour ne pas changer): ")
        password = input("Mot de passe (laisser vide pour ne pas changer): ")
        role_id = input("Rôle ID (1: admin, 2: support, 3: sales) (laisser vide pour ne pas changer): ")

        user_data = {}
        if full_name:
            user_data['full_name'] = full_name
        if email:
            user_data['email'] = email
        if password:
            user_data['password'] = password
        if role_id:
            user_data['role_id'] = role_id

        return user_data

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
