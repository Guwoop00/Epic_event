from typing import Callable, Dict

from sentry_config import sentry_exception_handler
from rich.console import Console
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from controllers.contract_controller import ContractController
from controllers.customer_controller import CustomerController
from controllers.event_controller import EventController
from controllers.user_controller import UserController
from utils.config import DATABASE_URL
from utils.jwtoken import TokenManager
from views.menu_view import MenuView
from views.user_view import UserView


class MainController:
    console = Console()

    def __init__(self):
        """
        Initializes the MainController with database, views, controllers, and token manager.
        """
        # Database initialization
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Views initialization
        self.menu_view = MenuView()
        self.user_view = UserView()

        # Controllers initialization
        self.user_controller = UserController(self.session)
        self.event_controller = EventController(self.session)
        self.customer_controller = CustomerController(self.session)
        self.contract_controller = ContractController(self.session)

        # Token manager initialization
        self.token_manager = TokenManager()

        # Action maps
        self.menu_actions = {
            1: self.main_menu,
            2: exit
        }
        self.database_actions = {
            1: self.customer_controller.display_all_customers,
            2: self.contract_controller.display_all_contracts,
            3: self.event_controller.display_all_events,
            4: self.main_menu
        }

    def build_action_map(self, role: str, user) -> Dict[int, Callable[[], None]]:
        """
        Builds an action map based on the user's role.

        :param role: The role of the user (admin, support, or sales)
        :param user: The user object
        :return: A dictionary mapping menu options to actions
        """
        action_map = {}
        if role == 'admin':
            action_map = {
                1: lambda: self.user_controller.create_user(user),
                2: lambda: self.user_controller.update_user(user),
                3: lambda: self.user_controller.delete_user(user),
                4: lambda: self.contract_controller.create_contract(user),
                5: lambda: self.event_controller.display_events(user),
                6: lambda: self.event_controller.add_support_to_event(user),
                7: lambda: self.user_controller.database(self.database_actions),
                8: self.user_controller.logout
            }
        elif role == 'support':
            action_map = {
                1: lambda: self.event_controller.display_events(user),
                2: lambda: self.event_controller.update_event(user),
                3: lambda: self.user_controller.database(self.database_actions),
                4: self.user_controller.logout
            }
        elif role == 'sales':
            action_map = {
                1: lambda: self.customer_controller.create_customer(user),
                2: lambda: self.customer_controller.update_customer(user),
                3: lambda: self.event_controller.create_event(user),
                4: lambda: self.contract_controller.update_contract(user),
                5: lambda: self.contract_controller.display_contracts(user),
                6: lambda: self.user_controller.database(self.database_actions),
                7: self.user_controller.logout
            }
        return action_map

    @sentry_exception_handler
    def login_menu(self) -> None:
        """
        Displays the login menu and handles login actions.
        """
        menu_option = self.menu_view.login_menu_options()
        self.menu_view.display_menu(menu_option, self.menu_actions)

    @sentry_exception_handler
    def main_menu(self) -> None:
        """
        Displays the main menu after user authentication.
        """
        username, password = self.user_view.input_login_view()
        user = self.user_controller.auth_user(username, password)

        if user:
            access_token = self.token_manager.create_token(user)
            self.token_manager.store_tokens(user.id, access_token)
            user_verified = self.token_manager.validate_token(access_token)

            if user_verified:
                self.user_view.authenticated_user_view()
                role = user.role.name.lower()
                menu_method_name = f"{role}_menu_options"
                menu_option = getattr(self.menu_view, menu_method_name)()
                action_map = self.build_action_map(role, user)
                self.menu_view.display_menu(menu_option, action_map)
            else:
                self.user_view.unauthenticated_user_view()
                self.login_menu()
        else:
            self.user_view.unauthenticated_user_view()
            self.login_menu()


if __name__ == "__main__":
    main_controller = MainController()
    main_controller.login_menu()
