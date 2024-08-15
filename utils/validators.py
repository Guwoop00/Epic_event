import re
from datetime import datetime
from getpass import getpass

from rich.console import Console

from models.models import Contract, Customer, Event, Role, User
from views.menu_view import MenuView


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

            if allow_empty and value.strip() == "":
                return None

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

    def transform_boolean(self, value) -> bool:
        valid_true = {"oui", "yes", "y"}
        valid_false = {"non", "no", "n"}

        if value in valid_true:
            return True

        if value in valid_false:
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
        value = int(value)
        if isinstance(value, int) and value >= 0:
            return True
        MenuView.validate_attendees_view()
        return False

    @staticmethod
    def convert_to_float(value):
        """Convertit une chaîne de caractères en float, ou renvoie None si la conversion échoue."""
        if isinstance(value, str):
            try:
                return float(value.replace(',', '.'))
            except ValueError:
                return None
        return value

    @staticmethod
    def validate_amount_total(amount_total) -> bool:
        amount_total = DataValidator.convert_to_float(amount_total)
        print(amount_total)

        if isinstance(amount_total, (int, float)) and amount_total >= 0.0:
            return True

        MenuView.validate_amount_total_view()
        return False

    @staticmethod
    def validate_amount_due(amount_due, amount_total) -> bool:
        amount_due = DataValidator.convert_to_float(amount_due)
        amount_total = DataValidator.convert_to_float(amount_total)
        print(amount_total)
        print(amount_due)

        if 0.0 <= amount_due <= amount_total:
            return True

        MenuView.validate_amount_due_view()
        return False

    @staticmethod
    def validate_boolean(value) -> bool:
        value = value.strip().lower()

        accepted_values = {"oui", "yes", "y", "non", "no", "n"}

        if value in accepted_values:
            return True

        else:
            MenuView.validate_boolean_view()
            raise ValueError("Invalid boolean value")

    @staticmethod
    def validate_date(value: str) -> bool:
        """
        Valide une date sous le format jj/mm/aaaa.
        :param value: Chaîne de caractères représentant une date.
        :return: True si la date est valide, sinon lève une exception ValueError.
        """
        date_format = "%d/%m/%Y"

        if not re.match(r"^\d{2}/\d{2}/\d{4}$", value):
            raise ValueError(f"Date format invalid: '{value}'. Expected format: 'jj/mm/aaaa'.")

        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            raise ValueError(f"Invalid date: '{value}'. Please enter a valid date in the format 'jj/mm/aaaa'.")
