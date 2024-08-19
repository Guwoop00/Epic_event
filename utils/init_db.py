import importlib
from getpass import getpass

from argon2 import PasswordHasher
from config import Base, SessionLocal, engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from validators import DataValidator

import views.user_view
from models.models import Role, User
from views.user_view import UserView

importlib.reload(views.user_view)


def init_db() -> None:
    """Creates the database tables and handles any SQLAlchemy errors."""
    try:
        Base.metadata.create_all(bind=engine)
        UserView.table_created_successfull()
    except SQLAlchemyError as e:
        UserView.table_creation_error(e)


def create_roles(session: Session) -> None:
    """Creates the default roles: Admin, Support, and Sales in the database if they do not exist."""
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


def create_admin_user(session: Session) -> str:
    """Creates a default admin user in the database and returns the admin's email."""
    ph = PasswordHasher()
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
        return ""


def prompt_change_password(session: Session, email: str) -> None:
    """Prompts the admin user to change the password and updates it in the database."""
    user = session.query(User).filter(User.email == email).first()
    UserView.prompt_change_password_view()
    new_password = getpass()
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


if __name__ == "__main__":
    with SessionLocal() as session:
        init_db()
        create_roles(session)
        email = create_admin_user(session)
        prompt_change_password(session, email)
