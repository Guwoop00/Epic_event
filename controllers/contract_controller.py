from datetime import date
from typing import List, Optional

from sentry_config import sentry_exception_handler
from sqlalchemy.orm import Session

from models.models import Contract
from utils.jwtoken import TokenManager
from utils.validators import DataValidator
from views.contract_view import ContractView
from views.menu_view import MenuView


class ContractController:
    def __init__(self, session: Session):
        """
        Initializes the contract controller.

        :param session: SQLAlchemy session object
        """
        self.session = session
        self.contract_view = ContractView()
        self.menu_view = MenuView()
        self.validators = DataValidator(session)
        self.token_manager = TokenManager()

    @sentry_exception_handler
    @TokenManager.token_required
    def create_contract(self, user) -> Optional[Contract]:
        """
        Creates a new contract.

        :param user: The user creating the contract
        :return: The created Contract object or None if creation fails
        """
        prompts = self.contract_view.get_create_contract_prompts()
        customer_id = self.validators.validate_input(prompts["customer_id"],
                                                     self.validators.validate_existing_customer_id)
        amount_total = self.validators.validate_input(prompts["amount_total"],
                                                      self.validators.validate_amount_total)
        amount_due = self.validators.validate_input(prompts["amount_due"],
                                                    lambda amount_due:
                                                    self.validators.validate_amount_due(amount_due, amount_total))
        is_signed = self.validators.validate_input(prompts["is_signed"], self.validators.validate_boolean)
        is_signed_bool = self.validators.transform_boolean(is_signed)

        contract = Contract(
            customer_id=customer_id,
            amount_total=amount_total,
            amount_due=amount_due,
            creation_date=date.today(),
            is_signed=is_signed_bool,
        )

        self.session.add(contract)
        self.session.commit()
        self.session.refresh(contract)
        self.contract_view.contract_created()
        return contract

    @sentry_exception_handler
    @TokenManager.token_required
    def update_contract(self, user) -> Optional[Contract]:
        """
        Updates an existing contract.

        :param user: The user updating the contract
        :return: The updated Contract object or None if the contract was not found or update fails
        """
        prompts = self.contract_view.contract_view_prompts()
        contract_id = self.validators.validate_input(prompts["contract_id"], lambda value:
                                                     self.validators.validate_existing_my_contract_id
                                                     (value, user))
        contract = self.get_contract(contract_id)

        if contract:
            prompts = self.contract_view.get_update_contract_prompts()
            customer_id = self.validators.validate_input(prompts["customer_id"],
                                                         self.validators.validate_existing_customer_id,
                                                         allow_empty=True)
            amount_total = self.validators.validate_input(prompts["amount_total"],
                                                          self.validators.validate_amount_total,
                                                          allow_empty=True)
            amount_due = self.validators.validate_input(prompts["amount_due"],
                                                        lambda amount_due:
                                                        self.validators.validate_amount_due
                                                        (amount_due, amount_total), allow_empty=True)
            is_signed = self.validators.validate_input(prompts["is_signed"],
                                                       self.validators.validate_boolean, allow_empty=True)
            is_signed_bool = self.validators.transform_boolean(is_signed)

            if customer_id:
                contract.customer_id = customer_id
            if amount_total:
                contract.amount_total = amount_total
            if amount_due:
                contract.amount_due = amount_due
            if is_signed:
                contract.is_signed = is_signed_bool

            self.session.commit()
            self.session.refresh(contract)
            self.contract_view.contract_updated()
        else:
            self.contract_view.contract_not_found()
        return contract

    @sentry_exception_handler
    @TokenManager.token_required
    def display_contracts(self, user) -> None:
        """
        Display filtered contracts.

        :param user: The user requesting the display of contracts
        """
        title, options = self.menu_view.filtered_contracts_menu_options()
        filter_option = self.menu_view.select_choice(title, options)
        contracts = self.get_filtered_contracts(filter_option)
        self.contract_view.display_contracts_view(contracts)

    @sentry_exception_handler
    def get_filtered_contracts(self, filter_option: int) -> List[Contract]:
        """
        Get filtered contracts based on the filter option.

        :param filter_option: The option to filter contracts
        :return: A list of Contract objects that match the filter criteria
        """
        if filter_option == 1:
            return self.session.query(Contract).filter(Contract.is_signed.is_(False)).all()
        elif filter_option == 2:
            return self.session.query(Contract).filter(Contract.amount_due > 0).all()
        elif filter_option == 3:
            return self.session.query(Contract).filter(Contract.is_signed.is_(True)).all()
        else:
            return self.session.query(Contract).all()

    @sentry_exception_handler
    def get_contract(self, contract_id: int) -> Optional[Contract]:
        """
        Gets a contract by ID.

        :param contract_id: The ID of the contract to retrieve
        :return: The Contract object with the specified ID or None if not found
        """
        return self.session.query(Contract).filter(Contract.id == contract_id).first()

    @sentry_exception_handler
    def display_all_contracts(self) -> None:
        """
        Display all contracts.
        """
        contracts = self.session.query(Contract).all()
        self.contract_view.display_contracts_view(contracts)
