import unittest
from unittest.mock import MagicMock, patch

from controllers.user_controller import UserController
from models.models import Base, Role, User
from utils.config import get_test_session, test_engine
from utils.jwtoken import TokenManager


class TestUserController(unittest.TestCase):

    def setUp(self):
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)

        self.session = next(get_test_session())
        self.user_controller = UserController(session=self.session)

        self.token_manager = TokenManager()
        self.user_controller.token_manager = self.token_manager

        self.user_view_mock = MagicMock()
        self.user_controller.user_view = self.user_view_mock

        self.mock_validator = MagicMock()
        self.user_controller.validators = self.mock_validator

    def tearDown(self):
        self.session.close()

    def create_authenticated_user(self, user_id=1, email="auth@ex.com", full_name="Auth User",
                                  password='Azerty13', role_name="UserRole"):
        hashed_password = self.user_controller.hash_password(password)
        role = Role(id=1, name=role_name)
        authenticated_user = User(id=user_id, email=email, full_name=full_name, password=hashed_password, role=role)

        self.session.add(role)
        self.session.add(authenticated_user)
        self.session.commit()

        return authenticated_user

    def create_mock_user(self, user_id=1, email="test@example.com", full_name="Test User", password="hashed_password"):
        """Helper method to create and persist a mock user"""
        mock_user = User(id=user_id, email=email, full_name=full_name, password=password)
        self.session.add(mock_user)
        self.session.commit()
        return mock_user

    def test_hash_password(self):
        password = "secure_password"
        hashed = self.user_controller.hash_password(password)
        self.assertNotEqual(password, hashed)

    def test_get_user_by_email(self):
        email = "test@example.com"
        mock_user = self.create_mock_user(email=email)

        user = self.user_controller.get_user_by_email(email)
        self.assertEqual(user.email, mock_user.email)

    def test_auth_user_success(self):
        email = "test@example.com"
        password = "secure_password"
        hashed_password = self.user_controller.hash_password(password)
        mock_user = self.create_mock_user(email=email, password=hashed_password)

        user = self.user_controller.auth_user(email, password)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, mock_user.email)

    def test_auth_user_incorrect_password(self):
        email = "test@example.com"
        password = "secure_password"
        wrong_password = "wrong_password"
        hashed_password = self.user_controller.hash_password(password)
        mock_user = self.create_mock_user(email=email, password=hashed_password)

        user = self.user_controller.auth_user(mock_user.email, wrong_password)
        self.assertIsNone(user)

    def test_create_user(self):
        authenticated_user = self.create_authenticated_user()
        self.mock_validator.validate_input.side_effect = ['Test User', 'test@example.com', 'password', 1]

        with patch.object(self.token_manager, 'get_tokens', return_value="fake_access_token"):
            with patch.object(self.token_manager, 'check_token', return_value=True):
                with patch.object(self.token_manager, 'validate_token', return_value=True):
                    with patch.object(self.user_controller, 'hash_password', return_value='hashed_password'):

                        user = self.user_controller.create_user(authenticated_user)
                        self.assertIsNotNone(user)
                        self.assertEqual(user.full_name, 'Test User')
                        self.session.commit()

    def test_update_user(self):
        authenticated_user = self.create_authenticated_user()
        self.mock_validator.validate_input.side_effect = [authenticated_user.id, 'New User',
                                                          'new@example.com', 'new_password', 1]

        with patch.object(self.token_manager, 'get_tokens', return_value="fake_access_token"):
            with patch.object(self.token_manager, 'check_token', return_value=True):
                with patch.object(self.token_manager, 'validate_token', return_value=True):

                    user = self.user_controller.update_user(authenticated_user)
                    self.assertIsNotNone(user)
                    self.assertEqual(user.full_name, 'New User')
                    self.session.commit()

    def test_delete_user(self):
        authenticated_user = self.create_authenticated_user()
        self.mock_validator.validate_input.side_effect = [authenticated_user.id]

        with patch.object(self.token_manager, 'get_tokens', return_value="fake_access_token"):
            with patch.object(self.token_manager, 'check_token', return_value=True):
                with patch.object(self.token_manager, 'validate_token', return_value=True):

                    deleted_user = self.user_controller.delete_user(authenticated_user)
                    self.assertIsNotNone(deleted_user)
                    self.assertEqual(deleted_user.id, authenticated_user.id)
                    self.session.commit()


if __name__ == '__main__':
    unittest.main()
