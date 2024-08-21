from unittest.mock import MagicMock


def test_create_contract(contract_controller, login_required_mock, mocker):
    user = MagicMock()
    contract_controller.validators.validate_input.side_effect = [1, 1000.0, 500.0, "y"]
    mock_transform_boolean = mocker.patch.object(contract_controller.validators, 'transform_boolean', return_value=True)
    contract = contract_controller.create_contract(user)

    assert contract is not None
    assert contract.amount_total == 1000.0
    mock_transform_boolean.assert_called_once()


def test_update_contract(contract_controller, create_contract, login_required_mock, mocker):
    user = MagicMock()
    contract = create_contract()
    contract_controller.validators.validate_input.side_effect = [1, 2, 1500.0, 750.0, "y"]
    mock_transform_boolean = mocker.patch.object(contract_controller.validators, 'transform_boolean', return_value=True)
    updated_contract = contract_controller.update_contract(user)

    assert contract is not None
    assert updated_contract is not None
    assert updated_contract.amount_total == 1500.0
    mock_transform_boolean.assert_called_once()


def test_get_filtered_contracts(contract_controller, create_contract):
    contract1 = create_contract(customer_id=1, amount_total=1000.0, amount_due=500.0, is_signed=False)
    contract2 = create_contract(customer_id=2, amount_total=2000.0, amount_due=0.0, is_signed=True)

    contracts = contract_controller.get_filtered_contracts(1)
    assert contract1 in contracts
    assert contract2 not in contracts

    contracts = contract_controller.get_filtered_contracts(2)
    assert contract1 in contracts
    assert contract2 not in contracts

    contracts = contract_controller.get_filtered_contracts(3)
    assert contract1 not in contracts
    assert contract2 in contracts

    contracts = contract_controller.get_filtered_contracts(4)
    assert contract1 in contracts
    assert contract2 in contracts


def test_get_contract(contract_controller, create_contract):
    contract = create_contract()
    fetched_contract = contract_controller.get_contract(contract.id)

    assert fetched_contract.id == contract.id
    assert fetched_contract.customer_id == contract.customer_id


def test_display_all_contracts(contract_controller, create_contract, mocker):
    contract1 = create_contract(customer_id=1, amount_total=1000.0, amount_due=500.0, is_signed=False)
    contract2 = create_contract(customer_id=2, amount_total=2000.0, amount_due=0.0, is_signed=True)

    mock_display = mocker.patch.object(contract_controller.contract_view, 'display_contracts_view')
    contract_controller.display_all_contracts()

    mock_display.assert_called_once_with([contract1, contract2])
