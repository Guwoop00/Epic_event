import re
from views.menu_view import MenuView
from rich.console import Console
from models.models import User, Customer, Event, Contract


class DataValidator:
    console = Console()

    def __init__(self, session):
        self.session = session

    def validate_input(self, prompt, validation_method, allow_empty=False):
        while True:
            value = input(prompt)
            if allow_empty and value == "":
                return None
            if validation_method(value):
                return value

    def validate_id(self) -> bool:
        title, options = MenuView.validate_id_view()
        choice = MenuView.select_choice(title, options)
        return choice

    def validate_existing_user_id(self, value: int, user_id: int) -> bool:
        user = self.session.query(User).filter(User.id == value).first()
        if user and (user.role.name != 'admin' or user.id == user_id):
            return True
        MenuView.validate_existing_user_id_view()
        return False

    def validate_existing_my_contract_id(self, value: int, user_id: int) -> bool:
        contract = self.session.query(Contract).filter(Contract.id == value).first()
        if contract and contract.customer.sales_contact_id == user_id:
            return True
        MenuView.validate_existing_contract_id_view()
        return False

    def validate_existing_customer_id(self, value: int) -> bool:
        customer = self.session.query(Customer).filter(Customer.id == value).first()
        if customer:
            return True
        MenuView.validate_existing_customer_id_view()
        return False

    def validate_existing_my_customer_id(self, value: int, user_id: int) -> bool:
        customer = self.session.query(Customer).filter(Customer.id == value).first()
        if customer and customer.sales_contact_id == user_id:
            return True
        MenuView.validate_existing_customer_id_view()
        return False

    def validate_existing_event_id(self, value: int) -> bool:
        event = self.session.query(Event).filter(Event.id == value).first()
        if event:
            return True
        MenuView.validate_existing_event_id_view()
        return False

    def validate_add_support_to_event(self, value: int) -> bool:
        user = self.session.query(User).filter(User.id == value).first()
        if user and user.role_id == 2:
            return True
        MenuView.validate_add_support_to_event_view()
        return False

    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < 8:
            MenuView.validate_eight_ch_password_view()
            return False
        if not re.search(r'[A-Z]', password):
            MenuView.validate_maj_password_view()
            return False
        if not re.search(r'[a-z]', password):
            MenuView.validate_min_password_view()
            return False
        if not re.search(r'[0-9]', password):
            MenuView.validate_num_password_view()
            return False
        return True

    @staticmethod
    def validate_str(value: str) -> bool:
        if isinstance(value, str) and value.strip():
            return True
        MenuView.validate_str_view()
        return False

    @staticmethod
    def validate_email(value: str) -> bool:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(pattern, value):
            return True
        MenuView.validate_email_view()
        return False

    @staticmethod
    def validate_phone(value: str) -> bool:
        pattern = r'^\+?\d{10,15}$'
        if re.match(pattern, value):
            return True
        MenuView.validate_phone_view()
        return False

    @staticmethod
    def validate_attendees(value: int) -> bool:
        if isinstance(value, int) and value >= 0:
            return True
        MenuView.validate_attendees_view()
        return False

    @staticmethod
    def validate_amount_total(amount_total: float) -> bool:
        if isinstance(amount_total, (int, float)) and amount_total >= 0.0:
            return True
        MenuView.validate_amount_total_view()
        return False

    @staticmethod
    def validate_amount_due(amount_due: float, amount_total: float) -> bool:
        if isinstance(amount_due, (int, float)) and amount_due >= 0.0 and amount_due <= amount_total:
            return True
        MenuView.validate_amount_due_view()
        return False

    @staticmethod
    def validate_boolean(value: str) -> bool:
        if value.lower() in ["true", "false"]:
            return True
        MenuView.validate_boolean_view()
        return False
