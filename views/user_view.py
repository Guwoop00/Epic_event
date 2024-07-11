class UserView:

    def input_login_view(self):
        print("Entrer vos identifiants")
        username = input("Email de connection: ")
        password = input("Mot de passe: ")
        return username, password

    def input_user_data(self):
        print("Créer un nouvel utilisateur")
        full_name = input("Nom complet: ")
        email = input("Email: ")
        password = input("Mot de passe: ")
        role_id = input("Rôle ID (1: admin, 2: support, 3: sales): ")
        return full_name, email, password, role_id

    def input_update_user_data(self):
        print("Mettre à jour l'utilisateur")
        full_name = input("Nom complet (laisser vide pour ne pas changer): ")
        email = input("Email (laisser vide pour ne pas changer): ")
        password = input("Mot de passe (laisser vide pour ne pas changer): ")
        role_id = input("Rôle ID (1: admin, 2: support, 3: sales) (laisser vide pour ne pas changer): ")

        user_data = {}
        if full_name:
            user_data['full_name'] = full_name
        if email:
            user_data['email'] = email
        if password:
            user_data['password'] = password
        if role_id:
            user_data['role_id'] = role_id

        return user_data

    def input_user_id(self):
        user_id = int(input("Entrez l'ID de l'utilisateur: "))
        return user_id

    def display_users_view(self, user):
        print(f"User ID: #{user.id}, Nom complet: {user.full_name}, Email: {user.email}, Rôle : {user.role.name}")

    def authenticated_user_view(self):
        print("Connexion réussie !")

    def unauthenticated_user_view(self):
        print("Utilisateur ou mot de passe incorrect !")
