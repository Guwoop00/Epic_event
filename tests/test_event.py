from datetime import date


def test_create_event(event_controller, test_login_required, mocker):
    user = mocker.MagicMock(id=1)
    mocker.patch.object(event_controller.validators, 'validate_input', side_effect=[
        'Product Launch', 1, date.today(), date.today(), 'New York', 50, 'Important event'
    ])

    event = event_controller.create_event(user)
    assert event is not None
    assert event.event_name == 'Product Launch'


def test_update_event(event_controller, create_mock_event, test_login_required, mocker):
    user = mocker.MagicMock(id=1)
    event = create_mock_event(event_name='Old Event', location='Old Location', attendees=10, notes='Old Notes')

    mocker.patch.object(event_controller.validators, 'validate_input', side_effect=[
        event.id, 'Updated Event', date.today(), date.today(), 'New Location', 20, 'Updated Notes', 1
    ])

    updated_event = event_controller.update_event(user)
    assert updated_event is not None
    assert updated_event.event_name == 'Updated Event'


def test_get_event(event_controller, create_mock_event, mocker):
    event = create_mock_event(event_name='Event A', location='Location A', attendees=10, notes='Notes A')

    fetched_event = event_controller.get_event(event.id)
    assert fetched_event.id == event.id
    assert fetched_event.event_name == 'Event A'


def test_display_all_events(event_controller, create_mock_event, mocker):
    event1 = create_mock_event(event_name='Event A', location='Location A', attendees=10, notes='Notes A')
    event2 = create_mock_event(event_name='Event B', location='Location B', attendees=20, notes='Notes B')

    mock_display = mocker.patch.object(event_controller.event_view, 'display_events_view')
    event_controller.display_all_events()
    mock_display.assert_called_once_with([event1, event2])


def test_add_support_to_event(event_controller, create_mock_event, test_login_required, mocker):
    user = mocker.MagicMock(id=1)
    event = create_mock_event(event_name='Event A', location='Location A', attendees=10, notes='Notes A')

    mocker.patch.object(event_controller.validators, 'validate_input', side_effect=[event.id, 2])

    updated_event = event_controller.add_support_to_event(user)
    assert updated_event is not None
