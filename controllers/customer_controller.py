from models.models import Customer
from views.customer_view import CustomerView
from sqlalchemy.orm import Session
from datetime import date


class CustomerController:
    def __init__(self, session: Session):
        self.session = session
        self.customer_view = CustomerView()

    def create_customer(self):
        full_name, email, phone, company_name = self.customer_view.input_customer_data()
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
        print("Client créé avec succès.")
        return customer

    def update_customer(self):
        customer_id = self.customer_view.input_customer_id()
        customer = self.get_customer(customer_id)
        if customer:
            customer_data = self.customer_view.input_update_customer_data()
            customer_data['last_update'] = date.today()
            for key, value in customer_data.items():
                setattr(customer, key, value)
            self.session.commit()
            self.session.refresh(customer)
            print("Client mis à jour avec succès.")
        else:
            print("Client non trouvé.")
        return customer

    def get_customer(self, customer_id: int):
        return self.session.query(Customer).filter(Customer.id == customer_id).first()

    def display_customers(self):
        customers = self.session.query(Customer).all()
        for customer in customers:
            self.customer_view.display_customers_view(customer)
