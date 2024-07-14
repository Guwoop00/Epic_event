from models.models import Contract
from views.contract_view import ContractView
from views.menu_view import MenuView
from sqlalchemy.orm import Session
from datetime import date
from rich.console import Console


class ContractController:
    console = Console()

    def __init__(self, session: Session):
        self.session = session
        self.contract_view = ContractView()
        self.menu_view = MenuView()

    def create_contract(self):
        customer_id, amount_total, amount_due, is_signed = self.contract_view.input_contract_data()

        contract = Contract(
            customer_id=customer_id,
            amount_total=amount_total,
            amount_due=amount_due,
            creation_date=date.today(),
            is_signed=is_signed,
        )

        self.session.add(contract)
        self.session.commit()
        self.session.refresh(contract)
        print("Contrat créé avec succès.")
        return contract

    def update_contract(self):
        contract_id = self.contract_view.input_contract_id()
        contract = self.get_contract(contract_id)
        if contract:
            contract_data = self.contract_view.input_update_contract_data()
            for key, value in contract_data.items():
                setattr(contract, key, value)
            self.session.commit()
            self.session.refresh(contract)
            print("Contrat mis à jour avec succès.")
        else:
            print("Contrat non trouvé.")
        return contract

    def delete_contract(self):
        contract_id = self.contract_view.input_contract_id()
        contract = self.get_contract(contract_id)
        if contract:
            self.session.delete(contract)
            self.session.commit()
            print("Contrat supprimé avec succès.")
        else:
            print("Contrat non trouvé.")
        return contract

    def display_contracts(self):
        title, options = self.menu_view.filtered_contact_menu_options()
        filter_option = self.menu_view.select_choice(title, options)
        contracts = self.get_filtered_contracts(filter_option)
        self.contract_view.display_contracts_view(contracts)

    def get_filtered_contracts(self, filter_option):
        if filter_option == 1:
            return self.session.query(Contract).filter(Contract.is_signed is False).all()
        elif filter_option == 2:
            return self.session.query(Contract).filter(Contract.amount_due > 0).all()
        elif filter_option == 3:
            return self.session.query(Contract).filter(Contract.is_signed is True).all()
        else:
            return self.session.query(Contract).all()

    def get_contract(self, contract_id: int):
        return self.session.query(Contract).filter(Contract.id == contract_id).first()
