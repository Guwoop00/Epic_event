from views.menu_view import MenuView
from views.user_view import UserView
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import DATABASE_URL, SessionLocal
from controllers.event_controller import EventController
from controllers.customer_controller import CustomerController
from controllers.contract_controller import ContractController
from controllers.user_controller import UserController
from rich.console import Console


class MainController:
    console = Console()

    def __init__(self):
        self.menu_view = MenuView()
        self.user_view = UserView()

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
        self.sales_actions = {
            1: self.customer_controller.create_customer,
            2: self.customer_controller.update_customer,
            3: self.event_controller.create_event,
            4: self.contract_controller.update_contract,
            5: self.contract_controller.display_contracts,
            6: lambda: self.user_controller.database(self.database_actions),
            7: self.user_controller.logout
        }
        self.support_actions = {
            1: self.event_controller.display_events,
            2: self.event_controller.update_event,
            3: lambda: self.user_controller.database(self.database_actions),
            4: self.user_controller.logout
        }
        self.admin_actions = {
            1: self.user_controller.create_user,
            2: self.user_controller.update_user,
            3: self.user_controller.delete_user,
            4: self.contract_controller.create_contract,
            5: self.contract_controller.delete_contract,
            6: self.event_controller.display_events,
            7: self.add_support_to_event,
            8: lambda: self.user_controller.database(self.database_actions),
            9: self.user_controller.logout
        }
        self.database_actions = {
            1: self.user_controller.display_users,
            2: self.customer_controller.display_customers,
            3: self.contract_controller.display_contracts,
            4: self.event_controller.display_events,
            5: exit
        }

    def login_menu(self):
        menu_option = self.menu_view.login_menu_options()
        action_map = self.menu_actions
        self.menu_view.display_menu(menu_option, action_map)

    def main_menu(self):
        username, password = self.user_view.input_login_view()
        with SessionLocal() as session:
            user = self.user_controller.auth_user(session, username, password)
            if user:
                self.user_view.authenticated_user_view()
                role = user.role.name.lower()
                menu_method_name = f"{role}_menu_options"
                action_map_name = f"{role}_actions"
                menu_option = getattr(self.menu_view, menu_method_name)()
                action_map = getattr(self, action_map_name)
                self.menu_view.display_menu(menu_option, action_map)
            else:
                self.user_view.unauthenticated_user_view()
                self.login_menu()

    def add_support_to_event(self):
        print("add support to event mode OK")


if __name__ == "__main__":
    main_controller = MainController()
    main_controller.login_menu()
