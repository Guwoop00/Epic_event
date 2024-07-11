class CustomerView:
    def input_customer_data(self):
        print("Créer un nouveau client")
        full_name = input("Nom complet: ")
        email = input("Email: ")
        phone = input("Téléphone: ")
        company_name = input("Nom de l'entreprise: ")
        return full_name, email, phone, company_name

    def input_update_customer_data(self):
        print("Mettre à jour le client")
        full_name = input("Nom complet (laisser vide pour ne pas changer): ")
        email = input("Email (laisser vide pour ne pas changer): ")
        phone = input("Téléphone (laisser vide pour ne pas changer): ")
        company_name = input("Nom de l'entreprise (laisser vide pour ne pas changer): ")

        customer_data = {}
        if full_name:
            customer_data['full_name'] = full_name
        if email:
            customer_data['email'] = email
        if phone:
            customer_data['phone'] = phone
        if company_name:
            customer_data['company_name'] = company_name

        return customer_data

    def input_customer_id(self):
        customer_id = int(input("Entrez l'ID du client: "))
        return customer_id

    def display_customers_view(self, customer):
        print(f"customer ID: #{customer.id}, Nom complet: {customer.full_name}, Email: {customer.email},"
              f"Téléphone: {customer.phone}, Entreprise: {customer.company_name}, "
              f"Contact commercial: {customer.sales_contact.full_name}")
