import re
from datetime import datetime
from getpass import getpass
from typing import Callable, Optional

from rich.console import Console
from sqlalchemy.orm import Session

from models.models import Contract, Customer, Event, Role, User
from views.menu_view import MenuView


class DataValidator:
    console = Console()

    def __init__(self, session: Session):
        """
        Initialize the DataValidator with a SQLAlchemy session.

        Args:
            session (Session): The SQLAlchemy session for database operations.
        """
        self.session = session

    def validate_input(self, prompt: str, validation_method: Callable, allow_empty: bool = False) -> Optional[str]:
        """
        Validate user input based on a given validation method.

        Args:
            prompt (str): The prompt to display to the user.
            validation_method (Callable): The method to validate the input.
            allow_empty (bool): Whether to allow empty input.

        Returns:
            Optional[str]: The validated input or None if empty input is allowed.
        """
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
        """
        Validate that a role ID exists in the database.

        Args:
            role_id (int): The role ID to validate.

        Returns:
            bool: True if the role ID is valid, False otherwise.
        """
        roles = self.session.query(Role).all()

        for role in roles:
            if role.id == role_id:
                return True

        MenuView.validate_role_id_view(role_id)
        return False

    def validate_existing_user_id(self, value: int, user_id: int) -> bool:
        """
        Validate that a user ID exists and belongs to an admin user (if applicable).

        Args:
            value (int): The user ID to validate.
            user_id (int): The current user's ID.

        Returns:
            bool: True if the user ID is valid, False otherwise.
        """
        user = self.session.query(User).filter(User.id == value).first()
        if user:
            if user.role.name == 'admin' and user.id != user_id:
                MenuView.user_role_error()
                return False
            return True
        MenuView.user_not_found_error()
        return False

    def validate_existing_my_contract_id(self, value: int, user_id: int) -> bool:
        """
        Validate that a contract ID exists and is assigned to the current user.

        Args:
            value (int): The contract ID to validate.
            user_id (int): The current user's ID.

        Returns:
            bool: True if the contract ID is valid and assigned to the user, False otherwise.
        """
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
        """
        Validate that a customer ID exists in the database.

        Args:
            value (int): The customer ID to validate.

        Returns:
            bool: True if the customer ID is valid, False otherwise.
        """
        if not value:
            MenuView.object_not_found_empty()
            return False
        customer = self.session.query(Customer).filter(Customer.id == value).first()
        if customer:
            return True
        MenuView.customer_not_found(value)
        return False

    def validate_existing_my_customer_id(self, value: int, user_id: int) -> bool:
        """
        Validate that a customer ID exists and is assigned to the current user.

        Args:
            value (int): The customer ID to validate.
            user_id (int): The current user's ID.

        Returns:
            bool: True if the customer ID is valid and assigned to the user, False otherwise.
        """
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
        """
        Validate that an event ID exists in the database.

        Args:
            value (int): The event ID to validate.

        Returns:
            bool: True if the event ID is valid, False otherwise.
        """
        if not value:
            MenuView.object_not_found_empty()
            return False
        event = self.session.query(Event).filter(Event.id == value).first()
        if event:
            return True
        MenuView.event_not_found(value)
        return False

    def validate_add_support_to_event(self, value: int) -> bool:
        """
        Validate that a user ID belongs to a support user.

        Args:
            value (int): The user ID to validate.

        Returns:
            bool: True if the user ID belongs to a support user, False otherwise.
        """
        user = self.session.query(User).filter(User.id == value).first()
        if user:
            if user.role_id == 2:
                return True
            else:
                MenuView.user_not_support(value)
        else:
            MenuView.user_not_found(value)
        return False

    def transform_boolean(self, value: str) -> bool:
        """
        Convert a string to a boolean.

        Args:
            value (str): The string value to convert.

        Returns:
            bool: True or False based on the string value.
        """
        valid_true = {"oui", "yes", "y"}
        valid_false = {"non", "no", "n"}

        if value.lower() in valid_true:
            return True

        if value.lower() in valid_false:
            return False

    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate a password for length, and required character types.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
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
        """
        Validate that a value is a non-empty string.

        Args:
            value (str): The value to validate.

        Returns:
            bool: True if the value is a valid string, False otherwise.
        """
        if isinstance(value, str) and value.strip():
            return True
        MenuView.invalid_string()
        return False

    @staticmethod
    def validate_email(value: str) -> bool:
        """
        Validate an email address format.

        Args:
            value (str): The email address to validate.

        Returns:
            bool: True if the email address is valid, False otherwise.
        """
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(pattern, value):
            return True
        MenuView.validate_email_view()
        return False

    @staticmethod
    def validate_phone(value: str) -> bool:
        """
        Validate a phone number format.

        Args:
            value (str): The phone number to validate.

        Returns:
            bool: True if the phone number is valid, False otherwise.
        """
        pattern = r'^\+?\d{10,15}$'
        if re.match(pattern, value):
            return True
        MenuView.validate_phone_view()
        return False

    @staticmethod
    def validate_attendees(value: int) -> bool:
        """
        Validate the number of attendees is a non-negative integer.

        Args:
            value (int): The number of attendees to validate.

        Returns:
            bool: True if the value is a valid number of attendees, False otherwise.
        """
        if isinstance(value, int) and value >= 0:
            return True
        MenuView.validate_attendees_view()
        return False

    @staticmethod
    def convert_to_float(value: str) -> Optional[float]:
        """
        Convert a string to a float.

        Args:
            value (str): The string to convert.

        Returns:
            Optional[float]: The converted float value or None if conversion fails.
        """
        if isinstance(value, str):
            try:
                return float(value.replace(',', '.'))
            except ValueError:
                return None
        return value

    @staticmethod
    def validate_amount_total(amount_total: str) -> bool:
        """
        Validate the total amount is a non-negative number.

        Args:
            amount_total (str): The amount total to validate.

        Returns:
            bool: True if the amount total is valid, False otherwise.
        """
        amount_total = DataValidator.convert_to_float(amount_total)
        if isinstance(amount_total, (int, float)) and amount_total >= 0.0:
            return True

        MenuView.validate_amount_total_view()
        return False

    @staticmethod
    def validate_amount_due(amount_due: str, amount_total: str) -> bool:
        """
        Validate that the amount due is within the total amount.

        Args:
            amount_due (str): The amount due to validate.
            amount_total (str): The total amount to compare against.

        Returns:
            bool: True if the amount due is valid, False otherwise.
        """
        amount_due = DataValidator.convert_to_float(amount_due)
        amount_total = DataValidator.convert_to_float(amount_total)

        if amount_due is not None and amount_total is not None and 0.0 <= amount_due <= amount_total:
            return True

        MenuView.validate_amount_due_view()
        return False

    @staticmethod
    def validate_boolean(value: str) -> bool:
        """
        Validate a string as a boolean value.

        Args:
            value (str): The string to validate.

        Returns:
            bool: True if the value is a valid boolean, False otherwise.
        """
        value = value.strip().lower()

        accepted_values = {"oui", "yes", "y", "non", "no", "n"}

        if value in accepted_values:
            return True

        MenuView.validate_boolean_view()
        raise ValueError("Invalid boolean value")

    @staticmethod
    def validate_date(value: str) -> bool:
        """
        Validate a date string in the format 'dd/mm/yyyy'.

        Args:
            value (str): The date string to validate.

        Returns:
            bool: True if the date is valid, False otherwise.
        """
        date_format = "%d/%m/%Y"

        if not re.match(r"^\d{2}/\d{2}/\d{4}$", value):
            raise ValueError(f"Date format invalid: '{value}'. Expected format: 'dd/mm/yyyy'.")

        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            raise ValueError(f"Invalid date: '{value}'. Please enter a valid date in the format 'dd/mm/yyyy'.")
