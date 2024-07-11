class ContractView:
    def input_contract_data(self):
        print("Créer un nouveau contrat")
        customer_id = int(input("ID du client: "))
        amount_total = float(input("Montant total: "))
        amount_due = float(input("Montant dû: "))
        is_signed = input("Signé (oui/non): ").lower() == 'oui'
        return customer_id, amount_total, amount_due, is_signed

    def input_update_contract_data(self):
        print("Mettre à jour le contrat")
        customer_id = input("ID du client (laisser vide pour ne pas changer): ")
        amount_total = input("Montant total (laisser vide pour ne pas changer): ")
        amount_due = input("Montant dû (laisser vide pour ne pas changer): ")
        is_signed = input("Signé (laisser vide pour ne pas changer): ")

        contract_data = {}
        if customer_id:
            contract_data['customer_id'] = int(customer_id)
        if amount_total:
            contract_data['amount_total'] = float(amount_total)
        if amount_due:
            contract_data['amount_due'] = float(amount_due)
        if is_signed:
            contract_data['is_signed'] = is_signed.lower() == 'oui'

        return contract_data

    def input_contract_id(self):
        contract_id = int(input("Entrez l'ID du contrat: "))
        return contract_id

    def display_contracts_view(self, contract):
        print(f"Contrat ID: #{contract.id}, "
              f"Nom du client: {contract.customer.full_name}, "
              f"Contact du client: {contract.customer.email}, {contract.customer.phone}, "
              f"Montant total: {contract.amount_total}, Montant dû: {contract.amount_due}$, "
              f"Signé: {contract.is_signed}")
