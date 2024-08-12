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

    def reauthenticate_user(self) -> Optional[Dict[str, str]]:
        """
        Prompts the user to re-enter their credentials to reauthenticate.
        """
        print("bonjour")
        email = self.user_view.prompt_email()
        password = self.user_view.prompt_password()
        return self.auth_user(email, password)

    @TokenManager.token_required
    def create_user(self, user) -> Optional[User]:
        """
        Creates a new user.
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

    @TokenManager.token_required
    def delete_user(self, user) -> Optional[User]:
        """
        Deletes an existing user.
        """
        try:
            prompts = self.user_view.user_view_prompts()
            user_id = self.validators.validate_input(prompts["user_id"], lambda value:
                                                     self.validators.validate_existing_user_id(value, user_id))
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

    def database(self, database_actions: Dict[int, Callable]) -> None:
        """
        Displays the database management menu.
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
        """
        try:
            self.token_manager.clear_cache(user.id)
        except Exception as e:
            sentry_sdk.capture_exception(e)
