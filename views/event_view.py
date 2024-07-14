from rich.console import Console
from rich.table import Table


class EventView:
    console = Console()

    def input_event_data(self):
        self.console.print("\n[bold yellow]Créer un nouvel événement[/bold yellow]\n")
        event_name = input("Nom de l'évenement: ")
        contract_id = int(input("ID du contrat: "))
        event_start_date = input("Date de début de l'événement (YYYY-MM-DD): ")
        event_end_date = input("Date de fin de l'événement (YYYY-MM-DD): ")
        location = input("Lieu: ")
        attendees = int(input("Nombre de participants: "))
        notes = input("Remarques: ")
        return event_name, event_start_date, event_end_date, location, attendees, notes, contract_id

    def input_update_event_data(self):
        self.console.print("\n[bold]Mettre à jour l'événement[/bold yellow]\n")
        event_start_date = input("Date de début de l'événement (YYYY-MM-DD, laisser vide pour ne pas changer): ")
        event_end_date = input("Date de fin de l'événement (YYYY-MM-DD, laisser vide pour ne pas changer): ")
        location = input("Lieu (laisser vide pour ne pas changer): ")
        attendees = input("Nombre de participants (laisser vide pour ne pas changer): ")
        notes = input("Remarques (laisser vide pour ne pas changer): ")
        contract_id = input("ID du contrat (laisser vide pour ne pas changer): ")

        event_data = {}
        if event_start_date:
            event_data['event_start_date'] = event_start_date
        if event_end_date:
            event_data['event_end_date'] = event_end_date
        if location:
            event_data['location'] = location
        if attendees:
            event_data['attendees'] = int(attendees)
        if notes:
            event_data['notes'] = notes
        if contract_id:
            event_data['contract_id'] = int(contract_id)

        return event_data

    def input_event_id(self):
        event_id = int(input("\nEntrez l'ID de l'événement: \n"))
        return event_id

    def display_events_view(self, event):
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
