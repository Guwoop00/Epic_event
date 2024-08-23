import pytest
from argon2.exceptions import VerifyMismatchError
from jwtoken import TokenManager


def test_hash_password(user_controller):
    password = "secure_password"
    hashed = user_controller.hash_password(password)
    assert password != hashed


def test_get_user_by_email(user_controller, create_mock_user):
    email = "test@example.com"
    mock_user = create_mock_user(email=email)

    user = user_controller.get_user_by_email(email)
    assert user.email == mock_user.email


def test_auth_user_success(user_controller, create_mock_user):
    email = "test@example.com"
    password = "secure_password"
    hashed_password = user_controller.hash_password(password)
    mock_user = create_mock_user(email=email, password=hashed_password)

    user = user_controller.auth_user(email, password)
    assert user is not None
    assert user.email == mock_user.email


def test_auth_user_incorrect_password(user_controller, create_mock_user):
    email = "test@example.com"
    password = "secure_password"
    wrong_password = "wrong_password"
    hashed_password = user_controller.hash_password(password)
    mock_user = create_mock_user(email=email, password=hashed_password)

    with pytest.raises(VerifyMismatchError):
        user = user_controller.auth_user(mock_user.email, wrong_password)

    user = None
    try:
        user = user_controller.auth_user(mock_user.email, wrong_password)
    except VerifyMismatchError:
        pass

    assert user is None


def test_create_user(user_controller, create_authenticated_user, login_required_mock, mocker):
    authenticated_user = create_authenticated_user()
    user_controller.validators.validate_input.side_effect = ['Test User', 'test@example.com', 'password', 1]

    mocker.patch.object(user_controller, 'hash_password', return_value='hashed_password')

    user = user_controller.create_user(authenticated_user)
    assert user is not None
    assert user.full_name == 'Test User'
    user_controller.session.commit()


def test_update_user(user_controller, create_authenticated_user, login_required_mock):
    authenticated_user = create_authenticated_user()
    user_controller.validators.validate_input.side_effect = [authenticated_user.id, 'New User',
                                                             'new@example.com', 'new_password', 1]

    user = user_controller.update_user(authenticated_user)
    assert user is not None
    assert user.full_name == 'New User'
    user_controller.session.commit()


def test_delete_user(user_controller, create_authenticated_user, login_required_mock):
    authenticated_user = create_authenticated_user()
    user_controller.validators.validate_input.side_effect = [authenticated_user.id]

    deleted_user = user_controller.delete_user(authenticated_user)
    assert deleted_user is not None
    assert deleted_user.id == authenticated_user.id
    user_controller.session.commit()


def test_decorator(mocker, create_authenticated_user, login_required_mock):
    function_to_test = lambda *x, **y: "executed"
    function_to_call = TokenManager.token_required(function_to_test)
    return_value = function_to_call(create_authenticated_user)
    assert return_value == "executed"