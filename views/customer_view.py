from rich.console import Console
from rich.table import Table


class CustomerView:
    console = Console()

    def get_create_customer_prompts(self):
        self.console.print("\n[bold yellow]Créer un nouveau client[/bold yellow]\n")
        prompts = {
            "full_name": "Nom complet: ",
            "email": "Email: ",
            "phone": "Téléphone: ",
            "company_name": "Nom de l'entreprise: "
        }
        return prompts

    def get_update_customer_prompts(self):
        self.console.print("\n[bold yellow]Mettre à jour le client[/bold yellow]\n")
        prompts = {
            "full_name": "Nom complet (laisser vide pour ne pas changer): ",
            "email": "Email (laisser vide pour ne pas changer): ",
            "phone": "Téléphone (laisser vide pour ne pas changer): ",
            "company_name": "Nom de l'entreprise (laisser vide pour ne pas changer): "
        }
        return prompts

    def input_customer_id(self):
        self.console.print("\n[bold yellow]Entrez l'ID du client:[/bold yellow]\n")
        customer_id = int(input("ID: "))
        return customer_id

    def display_customers_view(self, customers):
        table = Table(title="Détails du client")

        table.add_column("ID du client", header_style="bold cornflower_blue")
        table.add_column("Nom complet", header_style="bold cornflower_blue")
        table.add_column("Email", header_style="bold cornflower_blue")
        table.add_column("Téléphone", header_style="bold cornflower_blue")
        table.add_column("Entreprise", header_style="bold cornflower_blue")
        table.add_column("Contact commercial", header_style="bold cornflower_blue")

        for customer in customers:
            table.add_row(
                str(customer.id),
                customer.full_name,
                customer.email,
                customer.phone,
                customer.company_name,
                customer.sales_contact.full_name
            )

        self.console.print(table)

    def customer_created(self):
        self.console.print("\n[bold green]Client créé avec succès.[/bold green]\n")

    def customer_updated(self):
        self.console.print("\n[bold green]Client mis à jour avec succès.[/bold green]\n")

    def customer_not_found(self):
        self.console.print("\n[bold red]Client non trouvé.[/bold red]\n")
