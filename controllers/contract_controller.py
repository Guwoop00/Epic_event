import sentry_sdk
from models.models import Contract
from sqlalchemy.orm import Session
from views.contract_view import ContractView
from views.menu_view import MenuView
from utils.validators import DataValidator
from typing import Optional, List
from datetime import date


class ContractController:

    def __init__(self, session: Session):
        """
        Initializes the contract controller.

        :param session: SQLAlchemy Session
        """
        self.session = session
        self.contract_view = ContractView()
        self.menu_view = MenuView()
        self.validators = DataValidator(session)

    def create_contract(self) -> Optional[Contract]:
        """
        Creates a new contract.

        :return: The created contract
        """
        try:
            prompts = self.contract_view.get_create_contract_prompts()

            customer_id = self.validators.validate_input(prompts["customer_id"],
                                                         self.validators.validate_existing_customer_id)
            amount_total = self.validators.validate_input(prompts["amount_total"],
                                                          self.validators.validate_amount_total)
            amount_due = self.validators.validate_input(prompts["amount_due"], self.validators.validate_amount_due)
            is_signed = self.validators.validate_input(prompts["is_signed"], self.validators.validate_boolean)

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
            self.contract_view.contract_created()
            return contract

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None

    def update_contract(self) -> Optional[Contract]:
        """
        Updates an existing contract.

        :return: The updated contract or None if not found
        """
        try:
            prompts = self.contract_view.contract_view_prompts()

            contract_id = self.validators.validate_input(prompts["contract_id"],
                                                         self.validators.validate_existing_contract_id)
            contract = self.get_contract(contract_id)
            if contract:
                prompts = self.contract_view.get_update_user_prompts()
                customer_id = self.validators.validate_input(prompts["customer_id"],
                                                             self.validators.validate_existing_customer_id,
                                                             allow_empty=True)
                amount_total = self.validators.validate_input(prompts["amount_total"],
                                                              self.validators.validate_amount_total, allow_empty=True)
                amount_due = self.validators.validate_input(prompts["amount_due"],
                                                            self.validators.validate_amount_due, allow_empty=True)
                is_signed = self.validators.validate_input(prompts["is_signed"],
                                                           self.validators.validate_boolean, allow_empty=True)

                if customer_id:
                    contract.customer_id = customer_id
                if amount_total:
                    contract.amount_total = amount_total
                if amount_due:
                    contract.amount_due = amount_due
                if is_signed:
                    contract.is_signed = is_signed

                self.session.commit()
                self.session.refresh(contract)
                self.contract_view.contract_updated()
            else:
                self.contract_view.contract_not_found()
            return contract

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None

    def display_contracts(self):
        """
        Display filtered contracts.
        """
        try:
            title, options = self.menu_view.filtered_contracts_menu_options()
            filter_option = self.menu_view.select_choice(title, options)
            contracts = self.get_filtered_contracts(filter_option)
            self.contract_view.display_contracts_view(contracts)

        except Exception as e:
            sentry_sdk.capture_exception(e)

    def get_filtered_contracts(self, filter_option: int) -> List[Contract]:
        """
        Get filtered contracts.

        :param filter_option: Filter option choosen.
        :return: Filtered contracts.
        """
        try:
            if filter_option == 1:
                return self.session.query(Contract).filter(Contract.is_signed.is_(False)).all()
            elif filter_option == 2:
                return self.session.query(Contract).filter(Contract.amount_due > 0).all()
            elif filter_option == 3:
                return self.session.query(Contract).filter(Contract.is_signed.is_(True)).all()
            else:
                return self.session.query(Contract).all()

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None

    def get_contract(self, contract_id: int) -> Optional[Contract]:
        """
        Obtient un contrat par son ID.

        :param contract_id: L'ID du contrat
        :return: Le contrat ou None si non trouvé
        """
        try:
            return self.session.query(Contract).filter(Contract.id == contract_id).first()

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None

    def display_all_contracts(self):
        try:
            contracts = self.session.query(Contract).all()
            self.contract_view.display_contracts_view(contracts)

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None
