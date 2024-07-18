from views.menu_view import MenuView
from views.user_view import UserView
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utils.config import DATABASE_URL, SessionLocal
from controllers.event_controller import EventController
from controllers.customer_controller import CustomerController
from controllers.contract_controller import ContractController
from controllers.user_controller import UserController
from utils.jwtoken import TokenManager
from rich.console import Console
import sentry_sdk


class MainController:
    console = Console()

    def __init__(self):
        """
        Initializes the main controller with views, sub-controllers, and a database session.
        """
        self.menu_view = MenuView()
        self.user_view = UserView()
        self.token_manager = TokenManager()

        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.event_controller = EventController(self.session)
        self.customer_controller = CustomerController(self.session)
        self.contract_controller = ContractController(self.session)
        self.user_controller = UserController(self.session)

        self.menu_actions = {
            1: self.main_menu,
            2: exit
        }
        self.database_actions = {
            1: self.customer_controller.display_customers,
            2: self.contract_controller.display_all_contracts,
            3: self.event_controller.display_all_events,
            4: self.main_menu,
        }

    def build_action_map(self, role: str, user) -> dict:
        if role == 'admin':
            return {
                1: self.user_controller.create_user,
                2: self.user_controller.update_user,
                3: self.user_controller.delete_user,
                4: self.contract_controller.create_contract,
                5: lambda: self.event_controller.display_events(user),
                6: self.event_controller.add_support_to_event,
                7: lambda: self.user_controller.database(self.database_actions),
                8: self.user_controller.logout
            }
        elif role == 'support':
            return {
                1: lambda: self.event_controller.display_events(user),
                2: self.event_controller.update_event,
                3: lambda: self.user_controller.database(self.database_actions),
                4: self.user_controller.logout
            }
        elif role == 'sales':
            return {
                1: lambda: self.customer_controller.create_customer(user),
                2: self.customer_controller.update_customer,
                3: self.event_controller.create_event,
                4: self.contract_controller.update_contract,
                5: self.contract_controller.display_contracts,
                6: lambda: self.user_controller.database(self.database_actions),
                7: self.user_controller.logout
            }

        return {}

    def login_menu(self) -> None:
        """
        Displays the login menu and handles menu actions.
        """
        try:
            menu_option = self.menu_view.login_menu_options()
            action_map = self.menu_actions
            self.menu_view.display_menu(menu_option, action_map)

        except Exception as e:
            sentry_sdk.capture_exception(e)
            self.console.print(f"An error occurred: {e}")

    def main_menu(self) -> None:
        """
        Displays the main menu after user authentication.
        """
        try:
            username, password = self.user_view.input_login_view()
            with SessionLocal() as session:
                token = self.user_controller.auth_user(session, username, password)
                user_id = self.token_manager.validate_token(token, session)
                user = self.user_controller.get_user(user_id)

                if user:
                    self.user_view.authenticated_user_view()
                    role = user.role.name.lower()
                    menu_method_name = f"{role}_menu_options"
                    menu_option = getattr(self.menu_view, menu_method_name)()

                    action_map = self.build_action_map(role, user)
                    self.menu_view.display_menu(menu_option, action_map)
                else:
                    self.user_view.unauthenticated_user_view()
                    self.login_menu()

        except Exception as e:
            sentry_sdk.capture_exception(e)
            self.console.print(f"An error occurred: {e}")


if __name__ == "__main__":
    try:
        main_controller = MainController()
        main_controller.login_menu()

    except Exception as e:
        sentry_sdk.capture_exception(e)
        Console().print(f"An error occurred: {e}")
