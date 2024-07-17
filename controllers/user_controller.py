import sentry_sdk
from argon2 import PasswordHasher
from views.menu_view import MenuView
from views.user_view import UserView
from models.models import User
from sqlalchemy.orm import Session
from utils.jwtoken import TokenManager
from utils.validators import DataValidator
from typing import Optional, Dict, Callable


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

    def hash_password(self, password: str) -> str:
        """
        Hashes the user's password.

        :param password: Plain text password
        :return: Hashed password
        """
        ph = PasswordHasher()
        hashed_password = ph.hash(password)
        return hashed_password

    def get_user_by_email(self, session: Session, email: str) -> Optional[User]:
        """
        Retrieves a user by their email.

        :param session: SQLAlchemy Session
        :param email: User's email address
        :return: User or None
        """
        return session.query(User).filter(User.email == email).first()

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user by their ID.

        :param user_id: User's ID
        :return: User or None
        """
        return self.session.query(User).filter(User.id == user_id).first()

    def auth_user(self, session: Session, email: str, password: str) -> Optional[str]:
        """
        Authenticates a user with email and password.

        :param session: SQLAlchemy Session
        :param email: User's email address
        :param password: User's password
        :return: Authentication token or None
        """
        try:
            user = self.get_user_by_email(session, email)
            if not user:
                self.user_view.user_not_found()
                return None
            ph = PasswordHasher()
            try:
                if not ph.verify(user.password, password):
                    self.user_view.incorrect_password()
                    return None
            except Exception as e:
                sentry_sdk.capture_exception(e)
                return None

            token = self.token_manager.create_token(user)
            self.user_view.access_granted(token)
            return token

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None

    def create_user(self) -> Optional[User]:
        """
        Creates a new user.

        :return: The created user
        """
        try:
            prompts = self.user_view.get_create_user_prompts()

            full_name = self.validators.validate_input(prompts["full_name"], self.validators.validate_str)
            email = self.validators.validate_input(prompts["email"], self.validators.validate_email)
            password = self.validators.validate_input(prompts["password"], self.validators.validate_password)
            role_id = self.validators.validate_input(prompts["role_id"], self.validators.validate_id)

            hashed_password = self.hash_password(password)
            user = User(
                full_name=full_name,
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
            return None

    def update_user(self) -> Optional[User]:
        """
        Updates an existing user.

        :return: The updated user or None if not found
        """
        try:
            user_id = self.user_view.input_user_id()
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
                                                         self.validators.validate_id, allow_empty=True)

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
            return None

    def delete_user(self) -> Optional[User]:
        """
        Deletes an existing user.

        :return: The deleted user or None if not found
        """
        try:
            user_id = self.user_view.input_user_id()
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

    def display_users(self) -> None:
        """
        Displays the list of users.
        """
        try:
            users = self.session.query(User).all()
            self.user_view.display_users_view(users)

        except Exception as e:
            sentry_sdk.capture_exception(e)

    def database(self, database_actions: Dict[int, Callable]) -> None:
        """
        Displays the database management menu.

        :param database_actions: Dictionary of database actions
        """
        try:
            menu_option = self.menu_view.database_menu_options()
            self.menu_view.display_menu(menu_option, database_actions)

        except Exception as e:
            sentry_sdk.capture_exception(e)

    def logout(self) -> None:
        """
        Logs out the user.
        """
        try:
            print("Successfully logged out.")

        except Exception as e:
            sentry_sdk.capture_exception(e)
