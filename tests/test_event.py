import unittest
from unittest.mock import MagicMock, patch
from models.models import Event, Base
from controllers.event_controller import EventController
from utils.config import get_test_session, test_engine
from utils.jwtoken import TokenManager
from datetime import date


class TestEventController(unittest.TestCase):

    def setUp(self):
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)

        self.session = next(get_test_session())
        self.event_controller = EventController(session=self.session)

        self.token_manager = TokenManager()
        self.event_controller.token_manager = self.token_manager

        self.event_view_mock = MagicMock()
        self.event_controller.event_view = self.event_view_mock

        self.mock_validator = MagicMock()
        self.event_controller.validators = self.mock_validator

    def tearDown(self):
        self.session.close()

    def create_mock_event(self, event_name="Default Event", contract_id=1, event_start_date=date.today(),
                          event_end_date=date.today(), location="Default Location",
                          attendees=10, notes="Default Notes"):
        """Helper method to create and persist a mock event"""
        event = Event(event_name=event_name, contract_id=contract_id, event_start_date=event_start_date,
                      event_end_date=event_end_date, location=location, attendees=attendees, notes=notes)
        self.session.add(event)
        self.session.commit()
        return event

    def test_create_event(self):
        """Test event creation with mocked user input"""
        user = MagicMock(id=1)
        self.mock_validator.validate_input.side_effect = [
            'Product Launch', 1, date.today(), date.today(), 'New York', 50, 'Important event'
        ]

        with patch.object(self.token_manager, 'get_tokens', return_value=("fake_access_token")):
            with patch.object(self.token_manager, 'check_token', return_value=True):
                with patch.object(self.token_manager, 'validate_token', return_value=True):
                    event = self.event_controller.create_event(user)
                    self.assertIsNotNone(event)
                    self.assertEqual(event.event_name, 'Product Launch')

    def test_update_event(self):
        """Test event update with mocked user input"""
        user = MagicMock(id=1)
        event = self.create_mock_event(event_name='Old Event', location='Old Location', attendees=10, notes='Old Notes')

        self.mock_validator.validate_input.side_effect = [
            event.id, 'Updated Event', date.today(), date.today(), 'New Location', 20, 'Updated Notes', 1
        ]

        with patch.object(self.token_manager, 'get_tokens', return_value=("fake_access_token")):
            with patch.object(self.token_manager, 'check_token', return_value=True):
                with patch.object(self.token_manager, 'validate_token', return_value=True):
                    updated_event = self.event_controller.update_event(user)
                    self.assertIsNotNone(updated_event)
                    self.assertEqual(updated_event.event_name, 'Updated Event')

    def test_get_event(self):
        """Test retrieving an event by ID"""
        event = self.create_mock_event(event_name='Event A', location='Location A', attendees=10, notes='Notes A')

        fetched_event = self.event_controller.get_event(event.id)
        self.assertEqual(fetched_event.id, event.id)
        self.assertEqual(fetched_event.event_name, 'Event A')

    def test_display_all_events(self):
        """Test displaying all events"""
        event1 = self.create_mock_event(event_name='Event A', location='Location A', attendees=10, notes='Notes A')
        event2 = self.create_mock_event(event_name='Event B', location='Location B', attendees=20, notes='Notes B')

        with patch.object(self.event_controller.event_view, 'display_events_view') as mock_display:
            self.event_controller.display_all_events()
            mock_display.assert_called_once_with([event1, event2])

    def test_add_support_to_event(self):
        """Test adding support to an event"""
        user = MagicMock(id=1)
        event = self.create_mock_event(event_name='Event A', location='Location A', attendees=10, notes='Notes A')

        self.mock_validator.validate_input.side_effect = [
            event.id, 2
        ]

        with patch.object(self.token_manager, 'get_tokens', return_value=("fake_access_token")):
            with patch.object(self.token_manager, 'check_token', return_value=True):
                with patch.object(self.token_manager, 'validate_token', return_value=True):
                    updated_event = self.event_controller.add_support_to_event(user)
                    self.assertIsNotNone(updated_event)


if __name__ == '__main__':
    unittest.main()
