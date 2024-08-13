import unittest
from unittest.mock import MagicMock, patch
from models.models import Customer, Base
from controllers.customer_controller import CustomerController
from utils.config import get_test_session, test_engine
from utils.jwtoken import TokenManager


class TestCustomerController(unittest.TestCase):

    def setUp(self):
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)

        self.session = next(get_test_session())
        self.customer_controller = CustomerController(session=self.session)

        self.token_manager = TokenManager()
        self.customer_controller.token_manager = self.token_manager

        self.customer_view_mock = MagicMock()
        self.customer_controller.customer_view = self.customer_view_mock

        self.mock_validator = MagicMock()
        self.customer_controller.validators = self.mock_validator

    def tearDown(self):
        self.session.close()

    def create_mock_customer(self, full_name="John Doe", email="john.doe@example.com",
                             phone="1234567890", company_name="Doe Inc."):
        """Helper method to create and persist a mock customer"""
        customer = Customer(full_name=full_name, email=email, phone=phone, company_name=company_name)
        self.session.add(customer)
        self.session.commit()
        return customer

    def test_create_customer(self):
        """Test customer creation with mocked user input"""
        user = MagicMock(id=1)
        self.mock_validator.validate_input.side_effect = [
            'John Doe', 'john.doe@example.com', '1234567890', 'Doe Inc.', 1
        ]

        with patch.object(self.token_manager, 'get_tokens', return_value=("fake_access_token")):
            with patch.object(self.token_manager, 'check_token', return_value=True):
                with patch.object(self.token_manager, 'validate_token', return_value=True):
                    customer = self.customer_controller.create_customer(user)
                    self.assertIsNotNone(customer)
                    self.assertEqual(customer.full_name, 'John Doe')

    def test_update_customer(self):
        """Test customer update with mocked user input"""
        user = MagicMock()
        customer = self.create_mock_customer(full_name='Jane Doe', email='jane.doe@example.com',
                                             phone='0987654321', company_name='Doe Corp')

        self.mock_validator.validate_input.side_effect = [
            customer.id, 'Jane Smith', 'jane.smith@example.com', '1122334455', 'Smith Corp'
        ]

        with patch.object(self.token_manager, 'get_tokens', return_value=("fake_access_token")):
            with patch.object(self.token_manager, 'check_token', return_value=True):
                with patch.object(self.token_manager, 'validate_token', return_value=True):
                    updated_customer = self.customer_controller.update_customer(user)
                    self.assertIsNotNone(updated_customer)
                    self.assertEqual(updated_customer.full_name, 'Jane Smith')

    def test_get_customer(self):
        """Test getting a customer by ID"""
        customer = self.create_mock_customer(full_name='John Smith', email='john.smith@example.com',
                                             phone='1231231234', company_name='Smith Ltd')

        fetched_customer = self.customer_controller.get_customer(customer.id)
        self.assertEqual(fetched_customer.id, customer.id)
        self.assertEqual(fetched_customer.full_name, 'John Smith')


if __name__ == '__main__':
    unittest.main()
