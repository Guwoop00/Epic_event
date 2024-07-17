# init_db.py
from argon2 import PasswordHasher
from config import Base, SessionLocal, engine
from models.models import User, Role
from sqlalchemy.exc import SQLAlchemyError


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables créées avec succès.")
    except SQLAlchemyError as e:
        print(f"Erreur lors de la création des tables: {e}")


def create_admin_user():
    ph = PasswordHasher()
    with SessionLocal() as session:
        admin_role = session.query(Role).filter(Role.name == "admin").first()
        support_role = session.query(Role).filter(Role.name == "support").first()
        sales_role = session.query(Role).filter(Role.name == "sales").first()

        if not admin_role:
            admin_role = Role(name="admin")
            session.add(admin_role)
            session.commit()
            session.refresh(admin_role)

        if not support_role:
            support_role = Role(name="support")
            session.add(support_role)
            session.commit()
            session.refresh(support_role)

        if not sales_role:
            sales_role = Role(name="sales")
            session.add(sales_role)
            session.commit()
            session.refresh(sales_role)

        existing_user = session.query(User).filter(User.email == "admin@ex.com").first()
        existing_user1 = session.query(User).filter(User.email == "support@ex.com").first()
        existing_user2 = session.query(User).filter(User.email == "sales@ex.com").first()

        if existing_user:
            session.delete(existing_user)
            session.commit()

        if existing_user1:
            session.delete(existing_user1)
            session.commit()

        if existing_user2:
            session.delete(existing_user2)
            session.commit()

        hashed_password = ph.hash("adminpassword")
        user = User(
            full_name="Admin User",
            email="admin@ex.com",
            password=hashed_password,
            role_id=admin_role.id
        )
        session.add(user)
        session.commit()
        print("Utilisateur admin créé avec succès.")

        hashed_password = ph.hash("supportpassword")
        user1 = User(
            full_name="Support User",
            email="support@ex.com",
            password=hashed_password,
            role_id=support_role.id
        )
        session.add(user1)
        session.commit()
        print("Utilisateur support créé avec succès.")

        hashed_password = ph.hash("salespassword")
        user2 = User(
            full_name="Sales User",
            email="sales@ex.com",
            password=hashed_password,
            role_id=sales_role.id
        )
        session.add(user2)
        session.commit()
        print("Utilisateur sales créé avec succès.")


if __name__ == "__main__":
    init_db()
    create_admin_user()
