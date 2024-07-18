from rich.console import Console
from rich.table import Table


class ContractView:
    console = Console()

    def get_create_contract_prompts(self):
        self.console.print("\n[bold yellow]Créer un nouveau contrat[/bold yellow]\n")
        prompts = {
            "customer_id": "ID du client: ",
            "amount_total": "Montant total: ",
            "amount_due": "Montant dû: ",
            "is_signed": "Signé (oui/non): "
        }
        return prompts

    def get_update_contract_prompts(self):
        self.console.print("\n[bold yellow]Mettre à jour le contrat[/bold yellow]\n")
        prompts = {
            "customer_id": "ID du client (laisser vide pour ne pas changer): ",
            "amount_total": "Montant total (laisser vide pour ne pas changer): ",
            "amount_due": "Montant dû (laisser vide pour ne pas changer): ",
            "is_signed": "Signé (laisser vide pour ne pas changer): "
        }
        return prompts

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

    def contract_view_prompts(self):
        prompts = {
            "contract_id": "ID: "
        }
        return prompts

    def contract_created(self):
        self.console.print("\n[bold green]Contrat créé avec succès.[/bold green]\n")

    def contract_updated(self):
        self.console.print("\n[bold green]Contrat mis à jour avec succès.[/bold green]\n")

    def contract_deleted(self):
        self.console.print("\n[bold green]Contrat supprimé avec succès.[/bold green]\n")

    def contract_not_found(self):
        self.console.print("\n[bold red]Contrat non trouvé.[/bold red]\n")
