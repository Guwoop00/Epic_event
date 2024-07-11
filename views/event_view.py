class EventView:
    def input_event_data(self):
        print("Créer un nouvel événement")
        event_name = input("Nom de l'évenement: ")
        contract_id = int(input("ID du contrat: "))
        event_start_date = input("Date de début de l'événement (YYYY-MM-DD HH:MM:SS): ")
        event_end_date = input("Date de fin de l'événement (YYYY-MM-DD HH:MM:SS): ")
        location = input("Lieu: ")
        attendees = int(input("Nombre de participants: "))
        notes = input("Remarques: ")
        return event_name, event_start_date, event_end_date, location, attendees, notes, contract_id

    def input_update_event_data(self):
        print("Mettre à jour l'événement")
        event_start_date = input("Date de début de l'événement (YYYY-MM-DD HH:MM:SS,"
                                 "laisser vide pour ne pas changer): ")
        event_end_date = input("Date de fin de l'événement (YYYY-MM-DD HH:MM:SS, laisser vide pour ne pas changer): ")
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
        event_id = int(input("Entrez l'ID de l'événement: "))
        return event_id

    def display_events_view(self, event):
        print(f"Event ID: #{event.id}, Contrat ID: #{event.contract_id}, "
              f"Nom du client: {event.contract.customer.full_name}, "
              f"Contact du client: {event.contract.customer.email}, {event.contract.customer.phone}, "
              f"Début: {event.event_start_date}, Fin: {event.event_end_date}, "
              f"Lieu: {event.location}, Participants: {event.attendees}, Remarques: {event.notes}")
