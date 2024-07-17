from rich.console import Console
from rich.table import Table


class EventView:
    console = Console()

    def get_create_event_prompts(self):
        self.console.print("\n[bold yellow]Créer un nouvel événement[/bold yellow]\n")
        prompts = {
            "event_name": "Nom de l'événement: ",
            "contract_id": "ID du contrat: ",
            "event_start_date": "Date de début de l'événement (YYYY-MM-DD): ",
            "event_end_date": "Date de fin de l'événement (YYYY-MM-DD): ",
            "location": "Lieu: ",
            "attendees": "Nombre de participants: ",
            "notes": "Remarques (laisser vide pour ne pas changer): ",
        }
        return prompts

    def get_update_event_prompts(self):
        self.console.print("\n[bold yellow]Mettre à jour l'événement[/bold yellow]\n")
        prompts = {
            "event_name": "Nom de l'événement (laisser vide pour ne pas changer): ",
            "event_start_date": "Date de début de l'événement (YYYY-MM-DD, laisser vide pour ne pas changer): ",
            "event_end_date": "Date de fin de l'événement (YYYY-MM-DD, laisser vide pour ne pas changer): ",
            "location": "Lieu (laisser vide pour ne pas changer): ",
            "attendees": "Nombre de participants (laisser vide pour ne pas changer): ",
            "notes": "Remarques (laisser vide pour ne pas changer): ",
            "contract_id": "ID du contrat (laisser vide pour ne pas changer): "
        }
        return prompts

    def input_event_id(self):
        self.console.print("\n[bold yellow]Entrez l'ID de l'événement:[/bold yellow]\n")
        event_id = int(input("ID: "))
        return event_id

    def display_events_view(self, events):
        table = Table(title="Détails de l'événement")

        table.add_column("ID de l'événement", header_style="bold cornflower_blue")
        table.add_column("ID du contrat", header_style="bold cornflower_blue")
        table.add_column("Nom du client", header_style="bold cornflower_blue")
        table.add_column("Contact du client", header_style="bold cornflower_blue")
        table.add_column("Début", header_style="bold cornflower_blue")
        table.add_column("Fin", header_style="bold cornflower_blue")
        table.add_column("Lieu", header_style="bold cornflower_blue")
        table.add_column("Participants", header_style="bold cornflower_blue")
        table.add_column("Remarques", header_style="bold cornflower_blue")

        for event in events:
            table.add_row(
                str(event.id),
                str(event.contract_id),
                event.contract.customer.full_name,
                f"{event.contract.customer.email}, {event.contract.customer.phone}",
                str(event.event_start_date),
                str(event.event_end_date),
                event.location,
                str(event.attendees),
                event.notes
            )

        self.console.print(table)

    def event_created(self):
        self.console.print("\n[bold green]Événement créé avec succès.[/bold green]\n")

    def event_updated(self):
        self.console.print("\n[bold green]Événement mis à jour avec succès.[/bold green]\n")

    def event_not_found(self):
        self.console.print("\n[bold red]Événement non trouvé.[/bold red]\n")
