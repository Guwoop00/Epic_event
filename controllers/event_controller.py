import sentry_sdk
from models.models import Event
from views.event_view import EventView
from views.menu_view import MenuView
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional


class EventController:
    def __init__(self, session: Session):
        """
        Initializes the event controller.

        :param session: SQLAlchemy Session
        """
        self.session = session
        self.event_view = EventView()
        self.menu_view = MenuView()

    def create_event(self) -> Event:
        """
        Creates a new event.

        :return: The created event
        """
        try:
            prompts = self.event_view.get_create_event_prompts()

            event_name = self.validators.validate_input(prompts["event_name"], self.validators.validate_str)
            contract_id = self.validators.validate_input(prompts["contract_id"], self.validators.validate_id)
            event_start_date = self.validators.validate_input(prompts["event_start_date"],
                                                              self.validators.validate_date)
            event_end_date = self.validators.validate_input(prompts["event_end_date"], self.validators.validate_date)
            location = self.validators.validate_input(prompts["location"], self.validators.validate_str)
            attendees = self.validators.validate_input(prompts["attendees"], self.validators.validate_int)
            notes = self.validators.validate_input(prompts["notes"], self.validators.validate_str, allow_empty=True)

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
            self.event_view.event_created()
            return event

        except Exception as e:
            sentry_sdk.capture_exception(e)
        return None

    def update_event(self) -> Optional[Event]:
        """
        Updates an existing event.

        :return: The updated event or None if not found
        """
        try:
            event_id = self.event_view.input_event_id()
            event = self.get_event(event_id)

            if event:
                prompts = self.event_view.get_update_event_prompts()

                event_name = self.validators.validate_input(prompts["event_name"],
                                                            self.validators.validate_str, allow_empty=True)
                event_start_date = self.validators.validate_input(prompts["event_start_date"],
                                                                  self.validators.validate_date, allow_empty=True)
                event_end_date = self.validators.validate_input(prompts["event_end_date"],
                                                                self.validators.validate_date, allow_empty=True)
                location = self.validators.validate_input(prompts["location"],
                                                          self.validators.validate_str, allow_empty=True)
                attendees = self.validators.validate_input(prompts["attendees"],
                                                           self.validators.validate_int, allow_empty=True)
                notes = self.validators.validate_input(prompts["notes"], self.validators.validate_str, allow_empty=True)
                contract_id = self.validators.validate_input(prompts["contract_id"],
                                                             self.validators.validate_id, allow_empty=True)

                if event_name:
                    event.event_name = event_name
                if event_start_date:
                    event.event_start_date = event_start_date
                if event_end_date:
                    event.event_end_date = event_end_date
                if location:
                    event.location = location
                if attendees:
                    event.attendees = attendees
                if notes:
                    event.notes = notes
                if contract_id:
                    event.contract_id = contract_id

                self.session.commit()
                self.session.refresh(event)
                self.event_view.event_updated()
            else:
                self.event_view.event_not_found()
            return event

        except Exception as e:
            sentry_sdk.capture_exception(e)
        return None

    def get_event(self, event_id: int) -> Optional[Event]:
        """
        Retrieves an event by its ID.

        :param event_id: Event ID
        :return: Event or None
        """
        try:
            return self.session.query(Event).filter(Event.id == event_id).first()

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None

    def display_events(self):
        """
        Displays the list of events.
        """
        try:
            title, options = self.menu_view.filtered_event_menu_options()
            filter_option = self.menu_view.select_choice(title, options)
            events = self.get_filtered_events(filter_option)
            self.event_view.display_events_view(events)

        except Exception as e:
            sentry_sdk.capture_exception(e)

    def get_filtered_events(self, filter_option: int) -> List[Event]:
        """
        Get filtered events by choosen option.

        :param filter_option: Filter option choosen.
        :return: Filtered events list.
        """
        try:
            if filter_option == 1:
                return self.session.query(Event).filter(Event.support_contact_id.is_(None)).all()
            elif filter_option == 2:
                return self.session.query(Event).filter(Event.event_start_date > date.today()).all()
            elif filter_option == 3:
                return self.session.query(Event).filter(Event.event_end_date < date.today()).all()
            else:
                return self.session.query(Event).all()

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None
