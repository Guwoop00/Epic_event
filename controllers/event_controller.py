from models.models import Event
from views.event_view import EventView
from views.menu_view import MenuView
from sqlalchemy.orm import Session
from datetime import date
from rich.console import Console


class EventController:
    console = Console()

    def __init__(self, session: Session):
        self.session = session
        self.event_view = EventView()
        self.menu_view = MenuView()

    def create_event(self):
        event_name, event_start_date, event_end_date, location, attendees, notes, contract_id = self.event_view.input_event_data()

        event = Event(
            event_name=event_name,
            contract_id=contract_id,
            event_start_date=event_start_date,
            event_end_date=event_end_date,
            location=location,
            attendees=attendees,
            notes=notes,
        )

        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        print("Événement créé avec succès.")
        return event

    def update_event(self):
        event_id = self.event_view.input_event_id()
        event = self.get_event(event_id)
        if event:
            event_data = self.event_view.input_update_event_data()
            for key, value in event_data.items():
                setattr(event, key, value)
            self.session.commit()
            self.session.refresh(event)
            print("Événement mis à jour avec succès.")
        else:
            print("Événement non trouvé.")
        return event

    def get_event(self, event_id: int):
        return self.session.query(Event).filter(Event.id == event_id).first()

    def display_events(self):
        title, options = self.menu_view.filtered_event_menu_options()
        filter_option = self.menu_view.select_choice(title, options)
        events = self.get_filtered_events(filter_option)
        for event in events:
            self.event_view.display_events_view(event)

    def get_filtered_events(self, filter_option):
        if filter_option == 1:
            return self.session.query(Event).filter(Event.support_contact_id.is_(None)).all()
        elif filter_option == 2:
            return self.session.query(Event).filter(Event.event_start_date > date.today()).all()
        elif filter_option == 3:
            return self.session.query(Event).filter(Event.event_end_date < date.today()).all()
        else:
            return self.session.query(Event).all()
