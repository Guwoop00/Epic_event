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

        if not admin_role:
            admin_role = Role(name="admin")
            session.add(admin_role)
            session.commit()
            session.refresh(admin_role)

        existing_user = session.query(User).filter(User.email == "admin@ex.com").first()

        if existing_user:
            session.delete(existing_user)
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


if __name__ == "__main__":
    init_db()
    create_admin_user()
