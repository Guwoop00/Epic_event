import pytest
from unittest.mock import patch
from models.models import Role
from views.menu_view import MenuView


def test_validate_role_id(validator, session):
    """Test validate_role_id"""
    # Setup: Create a role in the database
    role = Role(id=1, name='Admin')
    session.add(role)
    session.commit()

    # Test with a valid role ID
    with patch.object(MenuView, 'validate_role_id_view') as mock_view:
        result = validator.validate_role_id(1)
        assert result is True
        mock_view.assert_not_called()

    # Test with an invalid role ID
    with patch.object(MenuView, 'validate_role_id_view') as mock_view:
        result = validator.validate_role_id(999)
        assert result is False
        mock_view.assert_called_once_with(999)


def test_validate_existing_user_id(validator, session, create_authenticated_user):
    """Test validate_existing_user_id"""
    mock_user = create_authenticated_user()

    # Test with existing user
    with patch.object(MenuView, 'user_not_found_error') as mock_view:
        result = validator.validate_existing_user_id(mock_user.id, mock_user.id)
        assert result is True
        mock_view.assert_not_called()

    # Test with non-existing user
    with patch.object(MenuView, 'user_not_found_error') as mock_view:
        result = validator.validate_existing_user_id(999, mock_user.id)
        assert result is False
        mock_view.assert_called_once()

    # Test with admin role mismatch
    mock_user.role.name = 'admin'
    with patch.object(MenuView, 'user_role_error') as mock_view:
        result = validator.validate_existing_user_id(mock_user.id, 999)
        assert result is False
        mock_view.assert_called_once()


def test_validate_existing_my_contract_id(validator, session, create_contract, create_mock_customer):
    """Test validate_existing_my_contract_id"""
    customer = create_mock_customer()
    contract = create_contract(customer_id=customer.id)
    customer.sales_contact_id = 1  # Assigning a sales contact

    # Test with valid contract and user
    with patch.object(MenuView, 'contract_not_assigned_to_user') as mock_view:
        result = validator.validate_existing_my_contract_id(contract.id, 1)
        assert result is True
        mock_view.assert_not_called()

    # Test with valid contract but wrong user
    with patch.object(MenuView, 'contract_not_assigned_to_user') as mock_view:
        result = validator.validate_existing_my_contract_id(contract.id, 2)
        assert result is False
        mock_view.assert_called_once()

    # Test with non-existing contract
    with patch.object(MenuView, 'contract_not_found') as mock_view:
        result = validator.validate_existing_my_contract_id(999, 1)
        assert result is False
        mock_view.assert_called_once()


def test_validate_existing_customer_id(validator, session, create_mock_customer):
    """Test validate_existing_customer_id"""
    customer = create_mock_customer()

    # Test with existing customer
    with patch.object(MenuView, 'customer_not_found') as mock_view:
        result = validator.validate_existing_customer_id(customer.id)
        assert result is True
        mock_view.assert_not_called()

    # Test with non-existing customer
    with patch.object(MenuView, 'customer_not_found') as mock_view:
        result = validator.validate_existing_customer_id(999)
        assert result is False
        mock_view.assert_called_once()


def test_validate_boolean(validator):
    """Test validate_boolean"""
    with patch.object(MenuView, 'validate_boolean_view') as mock_view:
        assert validator.validate_boolean('oui') is True
        assert validator.validate_boolean('non') is True
        mock_view.assert_not_called()

    # Test with invalid boolean value
    with patch.object(MenuView, 'validate_boolean_view') as mock_view:
        with pytest.raises(ValueError):
            validator.validate_boolean('maybe')
        mock_view.assert_called_once()


def test_validate_password(validator):
    """Test validate_password"""
    with patch.object(MenuView, 'password_too_short') as mock_view:
        assert validator.validate_password('Azerty13') is True
        assert validator.validate_password('Short1') is False
        mock_view.assert_called_once()

    with patch.object(MenuView, 'password_missing_uppercase') as mock_view:
        assert validator.validate_password('no_upper1') is False
        mock_view.assert_called_once()

    with patch.object(MenuView, 'password_missing_lowercase') as mock_view:
        assert validator.validate_password('NOLOWER1') is False
        mock_view.assert_called_once()

    with patch.object(MenuView, 'password_missing_number') as mock_view:
        assert validator.validate_password('NoNumber') is False
        mock_view.assert_called_once()


def test_validate_date(validator):
    """Test validate_date"""
    with pytest.raises(ValueError):
        validator.validate_date('32/01/2023')

    with pytest.raises(ValueError):
        validator.validate_date('29/02/2023')

    assert validator.validate_date('31/12/2023') is True


def test_validate_email(validator):
    """Test validate_email"""
    with patch.object(MenuView, 'validate_email_view') as mock_view:
        assert validator.validate_email('valid@example.com') is True
        assert validator.validate_email('invalid-email') is False
        mock_view.assert_called_once()


def test_validate_phone(validator):
    """Test validate_phone"""
    with patch.object(MenuView, 'validate_phone_view') as mock_view:
        assert validator.validate_phone('+123456789012') is True
        assert validator.validate_phone('12345') is False
        mock_view.assert_called_once()


def test_validate_amount_total(validator):
    """Test validate_amount_total"""
    with patch.object(MenuView, 'validate_amount_total_view') as mock_view:
        assert validator.validate_amount_total('1000') is True
        assert validator.validate_amount_total('-1000') is False
        mock_view.assert_called_once()


def test_validate_amount_due(validator):
    """Test validate_amount_due"""
    with patch.object(MenuView, 'validate_amount_due_view') as mock_view:
        assert validator.validate_amount_due('500', '1000') is True
        assert validator.validate_amount_due('1500', '1000') is False
        mock_view.assert_called_once()


def test_transform_boolean(validator):
    """Test transform_boolean"""
    assert validator.transform_boolean('oui') is True
    assert validator.transform_boolean('non') is False
    assert validator.transform_boolean('yes') is True
    assert validator.transform_boolean('no') is False
