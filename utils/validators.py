import re
from views.menu_view import MenuView
from rich.console import Console
from models.models import User, Customer, Event, Contract, Role
from getpass import getpass


class DataValidator:
    console = Console()

    def __init__(self, session):
        self.session = session

    def validate_input(self, prompt, validation_method, allow_empty=False):
        while True:
            if "Mot de passe" in prompt:
                value = getpass(prompt)
            else:
                value = input(prompt)

            # Retourner None si l'entrée est vide et allow_empty est True
            if allow_empty and value.strip() == "":
                return None

            # Valider l'entrée avec la méthode de validation fournie
            if validation_method(value):
                return value

    def validate_role_id(self, role_id: int) -> bool:
        roles = self.session.query(Role).all()

        for role in roles:
            if role.id == int(role_id):
                return True

        MenuView.validate_role_id_view(role_id)
        return False

    def validate_existing_user_id(self, value: int, user_id: int) -> bool:
        user = self.session.query(User).filter(User.id == value).first()
        if user:
            if user.role.name == 'admin' and user.id != user_id:
                MenuView.user_role_error()
                return False
            return True
        MenuView.user_not_found_error()
        return False

    def validate_existing_my_contract_id(self, value: int, user_id: int) -> bool:
        contract = self.session.query(Contract).filter(Contract.id == value).first()
        if contract:
            if contract.customer.sales_contact_id == user_id:
                return True
            else:
                MenuView.contract_not_assigned_to_user(value, user_id)
        else:
            MenuView.contract_not_found(value)
        return False

    def validate_existing_customer_id(self, value: int) -> bool:
        if not value:
            MenuView.object_not_found_empty()
            return False
        customer = self.session.query(Customer).filter(Customer.id == value).first()
        if customer:
            return True
        MenuView.customer_not_found(value)
        return False

    def validate_existing_my_customer_id(self, value: int, user_id: int) -> bool:
        customer = self.session.query(Customer).filter(Customer.id == value).first()
        if customer:
            if customer.sales_contact_id == user_id:
                return True
            else:
                MenuView.customer_not_assigned_to_user(value, user_id)
        else:
            MenuView.customer_not_found(value)
        return False

    def validate_existing_event_id(self, value: int) -> bool:
        if not value:
            MenuView.object_not_found_empty()
            return False
        event = self.session.query(Event).filter(Event.id == value).first()
        if event:
            return True
        MenuView.event_not_found(value)
        return False

    def validate_add_support_to_event(self, value: int) -> bool:
        user = self.session.query(User).filter(User.id == value).first()
        if user:
            if user.role_id == 2:
                return True
            else:
                MenuView.user_not_support(value)
        else:
            MenuView.user_not_found(value)
        return False

    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < 8:
            MenuView.password_too_short()
            return False
        if not re.search(r'[A-Z]', password):
            MenuView.password_missing_uppercase()
            return False
        if not re.search(r'[a-z]', password):
            MenuView.password_missing_lowercase()
            return False
        if not re.search(r'[0-9]', password):
            MenuView.password_missing_number()
            return False
        return True

    @staticmethod
    def validate_str(value: str) -> bool:
        if isinstance(value, str) and value.strip():
            return True
        MenuView.invalid_string()
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
    def validate_amount_total(amount_total) -> bool:
        if isinstance(amount_total, str):
            try:
                amount_total = float(amount_total.replace(',', '.'))
            except ValueError:
                MenuView.validate_amount_total_view()
                return False

        if isinstance(amount_total, (int, float)) and amount_total >= 0.0:
            return True
        MenuView.validate_amount_total_view()
        return False

    @staticmethod
    def validate_amount_due(amount_due, amount_total) -> bool:
        try:
            if isinstance(amount_due, str):
                amount_due = float(amount_due.replace(',', '.'))
            if isinstance(amount_total, str):
                amount_total = float(amount_total.replace(',', '.'))
        except ValueError:
            MenuView.validate_amount_due_view()
            return False

        if isinstance(amount_due, (int, float)) and isinstance(amount_total, (int, float)):
            if amount_due >= 0.0 and amount_due <= amount_total:
                return True

        MenuView.validate_amount_due_view()
        return False
