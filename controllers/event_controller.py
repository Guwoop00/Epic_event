from datetime import date
from typing import List, Optional

import sentry_sdk
from rich.console import Console
from sqlalchemy.orm import Session

from models.models import Event
from utils.jwtoken import TokenManager
from utils.validators import DataValidator
from views.event_view import EventView
from views.menu_view import MenuView


class EventController:
    console = Console()

    def __init__(self, session: Session):
        """
        Initializes the event controller.

        :param session: SQLAlchemy Session
        """
        self.session = session
        self.event_view = EventView()
        self.menu_view = MenuView()
        self.validators = DataValidator(session)
        self.token_manager = TokenManager()

    @TokenManager.token_required
    def create_event(self, user) -> Optional[Event]:
        """
        Creates a new event.

        :param user: The user creating the event
        :return: The created Event object or None if creation fails
        """
        try:
            prompts = self.event_view.get_create_event_prompts()

            event_name = self.validators.validate_input(prompts["event_name"], self.validators.validate_str)
            contract_id = self.validators.validate_input(prompts["contract_id"], lambda value:
                                                         self.validators.validate_existing_my_contract_id
                                                         (value, user.id))
            event_start_date = self.validators.validate_input(prompts["event_start_date"],
                                                              self.validators.validate_date)
            event_end_date = self.validators.validate_input(prompts["event_end_date"], self.validators.validate_date)
            location = self.validators.validate_input(prompts["location"], self.validators.validate_str)
            attendees = self.validators.validate_input(prompts["attendees"], self.validators.validate_attendees)
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
            print(e)
            return None

    @TokenManager.token_required
    def update_event(self, user) -> Optional[Event]:
        """
        Updates an existing event.

        :param user: The user updating the event
        :return: The updated Event object or None if the event was not found or update fails
        """
        try:
            prompts = self.event_view.event_view_prompts()

            event_id = self.validators.validate_input(prompts["event_id"], self.validators.validate_existing_event_id)
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
                                                           self.validators.validate_attendees, allow_empty=True)
                notes = self.validators.validate_input(prompts["notes"], self.validators.validate_str, allow_empty=True)

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

        :param event_id: The ID of the event to retrieve
        :return: The Event object with the specified ID or None if not found
        """
        try:
            return self.session.query(Event).filter(Event.id == event_id).first()

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None

    def display_all_events(self) -> None:
        """
        Displays all events.
        """
        try:
            events = self.session.query(Event).all()
            self.event_view.display_events_view(events)

        except Exception as e:
            sentry_sdk.capture_exception(e)

    @TokenManager.token_required
    def display_events(self, user) -> None:
        """
        Displays the list of events based on the user's role.

        :param user: The user requesting the display of events
        """
        try:
            if user.role.name.lower() == 'admin':
                title, options = self.menu_view.filtered_event_admin_menu_options()
                filter_option = self.menu_view.select_choice(title, options)
                events = self.get_admin_filtered_events(filter_option)

            elif user.role.name.lower() == 'support':
                title, options = self.menu_view.filtered_event_support_menu_options()
                filter_option = self.menu_view.select_choice(title, options)
                events = self.get_support_filtered_events(filter_option, user)

            self.event_view.display_events_view(events)

        except Exception as e:
            sentry_sdk.capture_exception(e)

    def get_admin_filtered_events(self, filter_option: int) -> List[Event]:
        """
        Get filtered events based on the selected option.

        :param filter_option: The option to filter events
        :return: A list of filtered Event objects
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
            return []

    def get_support_filtered_events(self, filter_option: int, user) -> List[Event]:
        """
        Get filtered events based on the selected option for support role.

        :param filter_option: The option to filter events
        :param user: The support user requesting the events
        :return: A list of filtered Event objects
        """
        try:
            if filter_option == 1:
                return self.session.query(Event).filter(Event.support_contact_id == user.id).all()
            else:
                return self.session.query(Event).all()

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return []

    @TokenManager.token_required
    def add_support_to_event(self, user) -> Optional[Event]:
        """
        Adds support to an event.

        :param user: The user adding support to the event
        :return: The updated Event object or None if the event was not found or update fails
        """
        try:
            prompts = self.event_view.event_view_prompts()
            event_id = self.validators.validate_input(prompts["event_id"], self.validators.validate_existing_event_id)
            event = self.get_event(event_id)

            if event:
                support_id = self.validators.validate_input(prompts["support_contact_id"],
                                                            self.validators.validate_add_support_to_event)

                if support_id:
                    event.support_contact_id = support_id
                    self.session.commit()
                    self.session.refresh(event)
                    self.event_view.event_updated()
                else:
                    self.event_view.event_not_created
            else:
                self.event_view.event_not_found()
            return event

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None
