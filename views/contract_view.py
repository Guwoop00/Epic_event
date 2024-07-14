from rich.console import Console
from rich.table import Table


class ContractView:
    console = Console()

    def input_contract_data(self):
        self.console.print("\n[bold yellow]Créer un nouveau contrat[/bold yellow]\n")
        customer_id = int(input("ID du client: "))
        amount_total = float(input("Montant total: "))
        amount_due = float(input("Montant dû: "))
        is_signed = input("Signé (oui/non): ").lower() == 'oui'
        return customer_id, amount_total, amount_due, is_signed

    def input_update_contract_data(self):
        self.console.print("\n[bold yellow]Mettre à jour le contrat[/bold yellow]\n")
        customer_id = input("ID du client (laisser vide pour ne pas changer): ")
        amount_total = input("Montant total (laisser vide pour ne pas changer): ")
        amount_due = input("Montant dû (laisser vide pour ne pas changer): ")
        is_signed = input("Signé (laisser vide pour ne pas changer): ")

        contract_data = {}
        if customer_id:
            contract_data['customer_id'] = int(customer_id)
        if amount_total:
            contract_data['amount_total'] = float(amount_total)
        if amount_due:
            contract_data['amount_due'] = float(amount_due)
        if is_signed:
            contract_data['is_signed'] = is_signed.lower() == 'oui'

        return contract_data

    def input_contract_id(self):
        contract_id = int(input("\nEntrez l'ID du contrat: \n"))
        return contract_id

    def display_contracts_view(self, contracts):
        table = Table(title="Détails du contrat")

        table.add_column("ID du contrat", header_style="bold cornflower_blue")
        table.add_column("Nom du client", header_style="bold cornflower_blue")
        table.add_column("Contact du client", header_style="bold cornflower_blue")
        table.add_column("Montant total", header_style="bold cornflower_blue")
        table.add_column("Montant dû", header_style="bold cornflower_blue")
        table.add_column("Signé", header_style="bold cornflower_blue")

        for contract in contracts:
            table.add_row(
                str(contract.id),
                contract.customer.full_name,
                f"{contract.customer.email}, {contract.customer.phone}",
                str(contract.amount_total),
                str(contract.amount_due),
                "Oui" if contract.is_signed else "Non"
            )

        self.console.print(table)
