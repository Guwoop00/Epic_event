from argon2 import PasswordHasher
from views.menu_view import MenuView
from views.user_view import UserView
from models.models import User
from sqlalchemy.orm import Session


class UserController:
    def __init__(self, session: Session):
        self.session = session
        self.menu_view = MenuView()
        self.user_view = UserView()

    def hash_password(self, password: str) -> str:
        ph = PasswordHasher()
        hashed_password = ph.hash(password)
        return hashed_password

    def get_user_by_email(self, session, email):
        return session.query(User).filter(User.email == email).first()

    def get_user(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    def auth_user(self, session, email, password):
        ph = PasswordHasher()
        user = self.get_user_by_email(session, email)
        if not user:
            return False
        try:
            if not ph.verify(user.password, password):
                return False
        except Exception:
            return False
        return user

    def create_user(self):
        full_name, email, password, role_id = self.user_view.input_user_data()
        hashed_password = self.hash_password(password)
        user = User(
            full_name=full_name,
            email=email,
            password=hashed_password,
            role_id=role_id
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        print("Utilisateur créé avec succès.")
        return user

    def update_user(self):
        user_id = self.user_view.input_user_id()
        user = self.get_user(user_id)
        if user:
            user_data = self.user_view.input_update_user_data()
            for key, value in user_data.items():
                setattr(user, key, value)
            self.session.commit()
            self.session.refresh(user)
            print("Utilisateur mis à jour avec succès.")
        else:
            print("Utilisateur non trouvé.")
        return user

    def delete_user(self):
        user_id = self.user_view.input_user_id()
        user = self.get_user(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            print("Utilisateur supprimé avec succès.")
        else:
            print("Utilisateur non trouvé.")
        return user

    def display_users(self):
        users = self.session.query(User).all()
        for user in users:
            self.user_view.display_users_view(user)

    def database(self, database_actions):
        menu_option = self.menu_view.database_menu_options()
        self.menu_view.display_menu(menu_option, database_actions)

    def logout(self):
        print("Déconnexion réussie.")
