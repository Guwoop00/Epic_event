from datetime import date
from typing import Optional

from sentry_config import sentry_exception_handler
from sqlalchemy.orm import Session

from models.models import Customer
from utils.jwtoken import TokenManager
from utils.validators import DataValidator
from views.customer_view import CustomerView
from views.menu_view import MenuView


class CustomerController:
    def __init__(self, session: Session):
        """
        Initializes the customer controller.

        :param session: SQLAlchemy Session
        """
        self.session = session
        self.customer_view = CustomerView()
        self.menu_view = MenuView()
        self.validators = DataValidator(session)
        self.token_manager = TokenManager()

    @sentry_exception_handler
    @TokenManager.token_required
    def create_customer(self, user) -> Optional[Customer]:
        """
        Creates a new customer.

        :param user: The user creating the customer
        :return: The created Customer object or None if creation fails
        """
        prompts = self.customer_view.get_create_customer_prompts()

        full_name = self.validators.validate_input(prompts["full_name"], self.validators.validate_str)
        email = self.validators.validate_input(prompts["email"], self.validators.validate_email)
        phone = self.validators.validate_input(prompts["phone"], self.validators.validate_phone)
        company_name = self.validators.validate_input(prompts["company_name"], self.validators.validate_str)
        creation_date = date.today()

        customer = Customer(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            creation_date=creation_date,
            sales_contact_id=user.id,
        )

        self.session.add(customer)
        self.session.commit()
        self.session.refresh(customer)
        self.customer_view.customer_created()
        return customer

    @sentry_exception_handler
    @TokenManager.token_required
    def update_customer(self, user) -> Optional[Customer]:
        """
        Updates an existing customer.

        :param user: The user updating the customer
        :return: The updated Customer object or None if the customer was not found or update fails
        """

        prompts = self.customer_view.customer_view_prompts()
        customer_id = self.validators.validate_input(prompts["customer_id"], lambda value:
                                                     self.validators.validate_existing_my_customer_id
                                                     (value, user.id))
        customer = self.get_customer(customer_id)

        if customer:
            prompts = self.customer_view.get_update_customer_prompts()
            full_name = self.validators.validate_input(prompts["full_name"],
                                                       self.validators.validate_str, allow_empty=True)
            email = self.validators.validate_input(prompts["email"],
                                                   self.validators.validate_email, allow_empty=True)
            phone = self.validators.validate_input(prompts["phone"], self.validators.validate_str, allow_empty=True)
            company_name = self.validators.validate_input(prompts["company_name"],
                                                          self.validators.validate_str, allow_empty=True)

            if full_name:
                customer.full_name = full_name
            if email:
                customer.email = email
            if phone:
                customer.phone = phone
            if company_name:
                customer.company_name = company_name
            customer.last_update = date.today()
            self.session.commit()
            self.session.refresh(customer)
            self.customer_view.customer_updated()

        else:
            self.customer_view.customer_not_found()

        return customer

    @sentry_exception_handler
    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """
        Retrieves a customer by their ID.

        :param customer_id: The ID of the customer to retrieve
        :return: The Customer object with the specified ID or None if not found
        """
        return self.session.query(Customer).filter(Customer.id == customer_id).first()

    @sentry_exception_handler
    def display_all_customers(self) -> None:
        """
        Displays the list of customers.
        """
        customers = self.session.query(Customer).all()
        self.customer_view.display_customers_view(customers)
