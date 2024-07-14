from rich.console import Console
from rich.table import Table


class CustomerView:
    console = Console()

    def input_customer_data(self):
        self.console.print("\n[bold yellow]Créer un nouveau client[/bold yellow]\n")
        full_name = input("Nom complet: ")
        email = input("Email: ")
        phone = input("Téléphone: ")
        company_name = input("Nom de l'entreprise: ")
        return full_name, email, phone, company_name

    def input_update_customer_data(self):
        self.console.print("\n[bold yellow]Mettre à jour le client[/bold yellow]\n")
        full_name = input("Nom complet (laisser vide pour ne pas changer): ")
        email = input("Email (laisser vide pour ne pas changer): ")
        phone = input("Téléphone (laisser vide pour ne pas changer): ")
        company_name = input("Nom de l'entreprise (laisser vide pour ne pas changer): ")

        customer_data = {}
        if full_name:
            customer_data['full_name'] = full_name
        if email:
            customer_data['email'] = email
        if phone:
            customer_data['phone'] = phone
        if company_name:
            customer_data['company_name'] = company_name

        return customer_data

    def input_customer_id(self):
        customer_id = int(input("\nEntrez l'ID du client: \n"))
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
