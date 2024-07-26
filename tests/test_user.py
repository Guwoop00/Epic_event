import pytest
from controllers.user_controller import UserController
from unittest.mock import patch, MagicMock


@pytest.fixture
def test_user_controller():
    session = MagicMock()
    return UserController(session)


def test_create_user(monkeypatch, test_user_controller):
    user_controller = test_user_controller

    monkeypatch.setattr(user_controller.user_view, 'get_create_user_prompts',
                        lambda: {
                            "full_name": "Nom complet: ",
                            "email": "Email: ",
                            "password": "Mot de passe: ",
                            "role_id": "Rôle ID (1: admin, 2: support, 3: sales): "
                        })

    inputs = iter(["Test User", "test@example.com", "Securepassword1", "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch.object(user_controller, 'hash_password', return_value='hashedpassword'):

        new_user = user_controller.create_user()
        print(new_user)

        user_controller.session.add.assert_called_once_with(new_user)

    assert new_user is not None, "L'utilisateur ne devrait pas être None"
    assert new_user.email == "test@example.com", "L'email de l'utilisateur doit correspondre"
    assert new_user.full_name == "Test User", "Le nom complet de l'utilisateur doit correspondre"
    assert new_user.role_id == 1, "L'ID de rôle de l'utilisateur doit correspondre"
