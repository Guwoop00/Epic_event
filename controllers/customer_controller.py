import sentry_sdk
from models.models import Customer
from views.customer_view import CustomerView
from sqlalchemy.orm import Session
from datetime import date


class CustomerController:

    def __init__(self, session: Session):
        """
        Initializes the customer controller.

        :param session: SQLAlchemy Session
        """
        self.session = session
        self.customer_view = CustomerView()

    def create_customer(self):
        """
        Creates a new customer.

        :return: The created customer
        """
        try:
            prompts = self.customer_view.get_create_customer_prompts()

            full_name = self.validators.validate_input(prompts["full_name"], self.validators.validate_str)
            email = self.validators.validate_input(prompts["email"], self.validators.validate_email)
            phone = self.validators.validate_input(prompts["phone"], self.validators.validate_str)
            company_name = self.validators.validate_input(prompts["company_name"], self.validators.validate_str)
            creation_date = date.today()

            customer = Customer(
                full_name=full_name,
                email=email,
                phone=phone,
                company_name=company_name,
                creation_date=creation_date,
                sales_contact_id=1,
            )

            self.session.add(customer)
            self.session.commit()
            self.session.refresh(customer)
            self.customer_view.customer_created()
            return customer

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None

    def update_customer(self):
        """
        Updates an existing customer.

        :return: The updated customer or None if not found
        """
        try:
            customer_id = self.customer_view.input_customer_id()
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

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None

    def get_customer(self, customer_id: int):
        """
        Retrieves a customer by their ID.

        :param customer_id: Customer ID
        :return: Customer or None
        """
        try:
            return self.session.query(Customer).filter(Customer.id == customer_id).first()

        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None

    def display_customers(self):
        """
        Displays the list of customers.
        """
        try:
            customers = self.session.query(Customer).all()
            self.customer_view.display_customers_view(customers)

        except Exception as e:
            sentry_sdk.capture_exception(e)
