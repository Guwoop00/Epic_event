

def test_create_customer(customer_controller, login_required_mock, mocker, create_mock_user):
    user = create_mock_user(user_id=1, email="test@example.com",
                            full_name="Test User", password="hashed_password")

    mocker.patch.object(customer_controller.validators, 'validate_input', side_effect=[
        'John Doe', 'john.doe@example.com', '1234567890', 'Doe Inc.', 1
    ])

    customer = customer_controller.create_customer(user)
    assert customer is not None
    assert customer.full_name == 'John Doe'


def test_update_customer(customer_controller, create_mock_customer, login_required_mock, mocker):
    user = mocker.MagicMock()

    customer = create_mock_customer(full_name='Jane Doe', email='jane.doe@example.com',
                                    phone='0987654321', company_name='Doe Corp')

    mocker.patch.object(customer_controller.validators, 'validate_input', side_effect=[
        customer.id, 'Jane Smith', 'jane.smith@example.com', '1122334455', 'Smith Corp'
    ])

    updated_customer = customer_controller.update_customer(user)

    assert updated_customer is not None
    assert updated_customer.full_name == 'Jane Smith'


def test_get_customer(customer_controller, create_mock_customer, mocker):

    customer = create_mock_customer(full_name='John Smith', email='john.smith@example.com',
                                    phone='1231231234', company_name='Smith Ltd')

    fetched_customer = customer_controller.get_customer(customer.id)

    assert fetched_customer.id == customer.id
    assert fetched_customer.full_name == 'John Smith'
