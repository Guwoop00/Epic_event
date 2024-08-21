from sentry_config import sentry_exception_handler
from rich.console import Console
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from controllers.contract_controller import ContractController
from controllers.customer_controller import CustomerController
from controllers.event_controller import EventController
from controllers.user_controller import UserController
from utils.config import DATABASE_URL
from utils.jwtoken import TokenManager, InvalidTokenException
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

    def build_action_map(self, role, user):
        """
        Builds the action map based on the user's role.
        """
        database_actions = {
            1: self.customer_controller.display_all_customers,
            2: self.contract_controller.display_all_contracts,
            3: self.event_controller.display_all_events,
            4: self.main_menu
        }

        action_maps = {
            "admin": {
                1: lambda: self.user_controller.create_user(user),
                2: lambda: self.user_controller.update_user(user),
                3: lambda: self.user_controller.delete_user(user),
                4: lambda: self.contract_controller.create_contract(user),
                5: lambda: self.event_controller.display_events(user),
                6: lambda: self.event_controller.add_support_to_event(user),
                7: lambda: self.user_controller.database(database_actions),
                8: self.user_controller.logout
            },
            "support": {
                1: lambda: self.event_controller.display_events(user),
                2: lambda: self.event_controller.update_event(user),
                3: lambda: self.user_controller.database(database_actions),
                4: self.user_controller.logout
            },
            "sales": {
                1: lambda: self.customer_controller.create_customer(user),
                2: lambda: self.customer_controller.update_customer(user),
                3: lambda: self.event_controller.create_event(user),
                4: lambda: self.contract_controller.update_contract(user),
                5: lambda: self.contract_controller.display_contracts(user),
                6: lambda: self.user_controller.database(database_actions),
                7: self.user_controller.logout
            }
        }

        # Default menu actions
        menu_actions = {
            1: self.main_menu,
            2: exit
        }

        return action_maps.get(role, menu_actions)

    @sentry_exception_handler
    def login_menu(self) -> None:
        """
        Displays the login menu and handles login actions.
        """
        self.menu_actions = {
            1: self.main_menu,
            2: exit
        }
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
            self.token_manager.store_tokens(access_token)
            user_verified = self.token_manager.validate_token(access_token)

            if user_verified:
                self.handle_menu_selection(user)
            else:
                self.user_view.unauthenticated_user_view()
                self.login_menu()
        else:
            self.user_view.unauthenticated_user_view()
            self.login_menu()

    @sentry_exception_handler
    def handle_menu_selection(self, user) -> None:
        """
        Handles the display and selection of menu options based on the user's role.
        """
        self.user_view.authenticated_user_view()
        role = user.role.name.lower()
        menu_method_name = f"{role}_menu_options"
        menu_option = getattr(self.menu_view, menu_method_name)()
        try:
            action_map = self.build_action_map(role, user)
            self.menu_view.display_menu(menu_option, action_map)
        except InvalidTokenException:
            self.login_menu()


if __name__ == "__main__":
    main_controller = MainController()
    main_controller.login_menu()
