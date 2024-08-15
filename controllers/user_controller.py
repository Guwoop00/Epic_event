from typing import Callable, Dict, Optional

import sentry_sdk
from argon2 import PasswordHasher
from sqlalchemy.orm import Session

from models.models import User
from utils.jwtoken import TokenManager
from utils.validators import DataValidator
from views.menu_view import MenuView
from views.user_view import UserView


class UserController:

    def __init__(self, session: Session):
        """
        Initializes the user controller.

        :param session: SQLAlchemy Session
        """
        self.session = session
        self.menu_view = MenuView()
        self.user_view = UserView()
        self.token_manager = TokenManager()
        self.validators = DataValidator(session)
        self.password_hasher = PasswordHasher()

    def hash_password(self, password: str) -> str:
        """
        Hashes the user's password.
        """
        return self.password_hasher.hash(password)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user by their email.
        """
        return self.session.query(User).filter(User.email == email).first()

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user by their ID.
        """
        return self.session.query(User).filter(User.id == user_id).first()

    def auth_user(self, email: str, password: str) -> Optional[Dict[str, str]]:
        """
        Authenticates a user with email and password.

        :param email: The email of the user
        :param password: The password of the user
        :return: A dictionary with user details if authentication is successful, None otherwise
        """
        try:
            user = self.get_user_by_email(email)

            if not user:
                self.user_view.user_not_found()
                return None

            if not self.password_hasher.verify(user.password, password):
                self.user_view.incorrect_password()
                return None

            return user

        except Exception as e:
            sentry_sdk.capture_exception(e)

    @TokenManager.token_required
    def create_user(self, user) -> Optional[User]:
        """
        Creates a new user.

        :param user: The user creating the new user (used for role verification)
        :return: The created User object or None if creation fails
        """
        try:
            prompts = self.user_view.get_create_user_prompts()
            full_name = self.validators.validate_input(prompts["full_name"],
                                                       self.validators.validate_str)
            email = self.validators.validate_input(prompts["email"],
                                                   self.validators.validate_email)
            password = self.validators.validate_input(prompts["password"],
                                                      self.validators.validate_password)
            role_id = self.validators.validate_input(prompts["role_id"],
                                                     self.validators.validate_role_id)
            hashed_password = self.hash_password(password)

            user = User(full_name=full_name,
                        email=email,
                        password=hashed_password,
                        role_id=role_id
                        )

            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            self.user_view.user_created()
            return user

        except Exception as e:
            sentry_sdk.capture_exception(e)

    @TokenManager.token_required
    def update_user(self, user) -> Optional[User]:
        """
        Updates an existing user.

        :param user: The user updating the existing user (used for role verification)
        :return: The updated User object or None if the user was not found or update fails
        """
        try:
            prompts = self.user_view.user_view_prompts()
            user_id = self.validators.validate_input(prompts["user_id"], lambda value:
                                                     self.validators.validate_existing_user_id(value, user.id))
            user = self.get_user(user_id)

            if user:
                prompts = self.user_view.get_update_user_prompts()
                full_name = self.validators.validate_input(prompts["full_name"],
                                                           self.validators.validate_str, allow_empty=True)
                email = self.validators.validate_input(prompts["email"],
                                                       self.validators.validate_email, allow_empty=True)
                password = self.validators.validate_input(prompts["password"],
                                                          self.validators.validate_password, allow_empty=True)
                role_id = self.validators.validate_input(prompts["role_id"],
                                                         self.validators.validate_role_id, allow_empty=True)

                if full_name:
                    user.full_name = full_name
                if email:
                    user.email = email
                if password:
                    user.password = self.hash_password(password)
                if role_id:
                    user.role_id = role_id

                self.session.commit()
                self.session.refresh(user)
                self.user_view.user_updated()
            else:
                self.user_view.user_not_found()
            return user

        except Exception as e:
            sentry_sdk.capture_exception(e)

    @TokenManager.token_required
    def delete_user(self, user) -> Optional[User]:
        """
        Deletes an existing user.

        :param user: The user performing the delete action (used for role verification)
        :return: The deleted User object or None if the user was not found or deletion fails
        """
        try:
            prompts = self.user_view.user_view_prompts()
            user_id = self.validators.validate_input(prompts["user_id"], lambda value:
                                                     self.validators.validate_existing_user_id(value, user.id))
            user = self.get_user(user_id)

            if user:
                self.session.delete(user)
                self.session.commit()
                self.user_view.user_deleted()
            else:
                self.user_view.user_not_found()
            return user

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None

    def database(self, database_actions: Dict[int, Callable[[], None]]) -> None:
        """
        Displays the database management menu.

        :param database_actions: A dictionary of menu options and corresponding action functions
        """
        try:
            menu_option = self.menu_view.database_menu_options()
            self.menu_view.display_menu(menu_option, database_actions)

        except Exception as e:
            sentry_sdk.capture_exception(e)

    @TokenManager.token_required
    def logout(self, user) -> None:
        """
        Logs out the user.

        :param user: The user to log out
        """
        try:
            self.token_manager.clear_cache(user.id)
        except Exception as e:
            sentry_sdk.capture_exception(e)
