from argon2 import PasswordHasher
from sqlalchemy.exc import SQLAlchemyError
from config import Base, SessionLocal, engine
from models.models import User, Role
from validators import DataValidator
from views.user_view import UserView

with SessionLocal() as session:

    def init_db():
        """Creates the database tables."""
        try:
            Base.metadata.create_all(bind=engine)
            UserView.table_created_successfull()

        except SQLAlchemyError as e:
            UserView.table_creation_error(e)

    def create_roles():
        """Creates the default roles: Admin, Support, and Sales."""
        try:
            roles = ["admin", "support", "sales"]
            for role_name in roles:
                existing_role = session.query(Role).filter(Role.name == role_name).first()
                if not existing_role:
                    role = Role(name=role_name)
                    session.add(role)

                    UserView.role_created_successfull(role_name)
            session.commit()
        except SQLAlchemyError as e:
            UserView.role_creation_error(e)

    def create_admin_user():
        """Creates a default admin user."""
        ph = PasswordHasher()
        with SessionLocal() as session:
            try:
                existing_user = session.query(User).filter(User.email == "admin@ex.com").first()

                if existing_user:
                    session.delete(existing_user)
                    session.commit()

                hashed_password = ph.hash("adminpassword")

                user = User(
                    full_name="Admin User",
                    email="admin@ex.com",
                    password=hashed_password,
                    role_id=1
                )
                session.add(user)
                session.commit()

                UserView.admin_user_created_successfull()
                return user.email

            except SQLAlchemyError as e:
                UserView.admin_user_created_error(e)

    def prompt_change_password(email):
        user = session.query(User).filter(User.email == email).first()

        UserView.prompt_change_password_view()
        new_password = input()

        try:
            # Validate the new password
            DataValidator.validate_password(new_password)
            ph = PasswordHasher()
            hashed_password = ph.hash(new_password)
            user.password = hashed_password
            session.commit()

            UserView.password_updated_successfull()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()


if __name__ == "__main__":
    init_db()
    create_roles()
    email = create_admin_user()
    prompt_change_password(email)
