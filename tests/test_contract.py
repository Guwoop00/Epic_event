import unittest
from unittest.mock import MagicMock, patch
from models.models import Contract, Base
from controllers.contract_controller import ContractController
from utils.config import get_test_session, test_engine
from utils.jwtoken import TokenManager


class TestContractController(unittest.TestCase):

    def setUp(self):
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)

        self.session = next(get_test_session())
        self.contract_controller = ContractController(session=self.session)

        self.token_manager = TokenManager()
        self.contract_controller.token_manager = self.token_manager

        self.contract_view_mock = MagicMock()
        self.contract_controller.contract_view = self.contract_view_mock

        self.mock_validator = MagicMock()
        self.contract_controller.validators = self.mock_validator

    def tearDown(self):
        self.session.close()

    def create_contract(self, customer_id=1, amount_total=1000.0, amount_due=500.0, is_signed=False):
        """Helper method to create and persist a contract"""
        contract = Contract(customer_id=customer_id, amount_total=amount_total,
                            amount_due=amount_due, is_signed=is_signed)
        self.session.add(contract)
        self.session.commit()
        return contract

    def test_create_contract(self):
        """Test contract creation with mocked user input"""
        user = MagicMock()
        self.mock_validator.validate_input.side_effect = [1, 1000.0, 500.0, True]

        with patch.object(self.token_manager, 'get_tokens', return_value="fake_access_token"):
            with patch.object(self.token_manager, 'check_token', return_value=True):
                with patch.object(self.token_manager, 'validate_token', return_value=True):
                    contract = self.contract_controller.create_contract(user)
                    self.assertIsNotNone(contract)
                    self.assertEqual(contract.amount_total, 1000.0)

    def test_update_contract(self):
        """Test contract update with mocked user input"""
        user = MagicMock()
        contract = self.create_contract()
        self.mock_validator.validate_input.side_effect = [1, 2, 1500.0, 750.0, True]

        with patch.object(self.token_manager, 'get_tokens', return_value="fake_access_token"):
            with patch.object(self.token_manager, 'check_token', return_value=True):
                with patch.object(self.token_manager, 'validate_token', return_value=True):
                    updated_contract = self.contract_controller.update_contract(user)
                    self.assertIsNotNone(contract)
                    self.assertIsNotNone(updated_contract)
                    self.assertEqual(updated_contract.amount_total, 1500.0)

    def test_get_filtered_contracts(self):
        """Test getting filtered contracts"""
        contract1 = self.create_contract(customer_id=1, amount_total=1000.0, amount_due=500.0, is_signed=False)
        contract2 = self.create_contract(customer_id=2, amount_total=2000.0, amount_due=0.0, is_signed=True)

        contracts = self.contract_controller.get_filtered_contracts(1)
        self.assertIn(contract1, contracts)
        self.assertNotIn(contract2, contracts)

        contracts = self.contract_controller.get_filtered_contracts(2)
        self.assertIn(contract1, contracts)
        self.assertNotIn(contract2, contracts)

        contracts = self.contract_controller.get_filtered_contracts(3)
        self.assertNotIn(contract1, contracts)
        self.assertIn(contract2, contracts)

    def test_get_contract(self):
        """Test getting a contract by ID"""
        contract = self.create_contract()

        fetched_contract = self.contract_controller.get_contract(contract.id)
        self.assertEqual(fetched_contract.id, contract.id)
        self.assertEqual(fetched_contract.customer_id, contract.customer_id)

    def test_display_all_contracts(self):
        """Test displaying all contracts"""
        contract1 = self.create_contract(customer_id=1, amount_total=1000.0, amount_due=500.0, is_signed=False)
        contract2 = self.create_contract(customer_id=2, amount_total=2000.0, amount_due=0.0, is_signed=True)

        with patch.object(self.contract_controller.contract_view, 'display_contracts_view') as mock_display:
            self.contract_controller.display_all_contracts()
            mock_display.assert_called_once_with([contract1, contract2])


if __name__ == '__main__':
    unittest.main()
