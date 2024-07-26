import re
from views.menu_view import MenuView
from rich.console import Console
from datetime import datetime
from models.models import User, Role, Customer, Event, Contract


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

    def validate_id(self, value: int) -> bool:
        roles = self.session.query(Role).all()
        valid_ids = [role.id for role in roles]

        if value in valid_ids:
            return True
        role_details = ', '.join([f"{role.id}: {role.name} " for role in roles])
        MenuView.validate_id_view(role_details)
        return False

    def validate_existing_user_id(self, value: int) -> bool:
        user = self.session.query(User).filter(User.id == value).first()
        if user:
            return True
        MenuView.validate_existing_user_id_view()
        return False

    def validate_existing_contract_id(self, value: int) -> bool:
        contract = self.session.query(Contract).filter(Contract.id == value).first()
        if contract:
            return True
        MenuView.validate_existing_contract_id_view()
        return False

    def validate_existing_customer_id(self, value: int) -> bool:
        customer = self.session.query(Customer).filter(Customer.id == value).first()
        if customer:
            return True
        MenuView.validate_existing_customer_id_view()
        return False

    def validate_existing_event_id(self, value: int) -> bool:
        event = self.session.query(Event).filter(Event.id == value).first()
        if event:
            return True
        MenuView.validate_existing_event_id_view()
        return False

    def validate_existing_role_id(self, value: int) -> bool:
        role = self.session.query(Role).filter(Role.id == value).first()
        if role:
            return True
        MenuView.validate_existing_role_id_view()
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
        DataValidator.console.print("[bold red]Chaîne de caractères non valide.[/bold red]")
        return False

    @staticmethod
    def validate_email(value: str) -> bool:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(pattern, value):
            return True
        DataValidator.console.print("[bold red]Email non valide.[/bold red]")
        return False

    @staticmethod
    def validate_phone(value: str) -> bool:
        pattern = r'^\+?\d{10,15}$'
        if re.match(pattern, value):
            return True
        DataValidator.console.print("[bold red]Numéro de téléphone non valide.[/bold red]")
        return False

    @staticmethod
    def validate_attendees(value: int) -> bool:
        if isinstance(value, int) and value >= 0:
            return True
        DataValidator.console.print("[bold red] Nombre de participants non valide.[/bold red]")
        return False

    @staticmethod
    def validate_amount_total(amount_total: float) -> bool:
        if isinstance(amount_total, (int, float)) and amount_total >= 0.0:
            return True
        print("[bold red]Montant total non valide.[/bold red]")
        return False

    @staticmethod
    def validate_amount_due(amount_due: float, amount_total: float) -> bool:
        if isinstance(amount_due, (int, float)) and amount_due >= 0.0 and amount_due <= amount_total:
            return True
        print("[bold red]Montant dû non valide.[/bold red]")
        return False

    @staticmethod
    def validate_datetime(value: str) -> bool:
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            DataValidator.console.print("[bold red]Date et heure non valides.[/bold red]")
            return False

    @staticmethod
    def validate_boolean(value: str) -> bool:
        if value.lower() in ["true", "false"]:
            return True
        print("[bold red]Merci de choisir parmis 'True' or 'False'.[/bold red]")
        return False
