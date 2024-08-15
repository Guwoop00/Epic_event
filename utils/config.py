import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

Base = declarative_base()
SECRET_KEY = os.getenv("SECRET_KEY")

DB = {
    "ENGINE": os.getenv("DB_ENGINE"),
    "HOST": os.getenv("DB_HOST"),
    "PORT": os.getenv("DB_PORT"),
    "NAME": os.getenv("DB_NAME"),
    "USER": os.getenv("DB_USER"),
    "PASSWORD": os.getenv("DB_PASSWORD"),
}

DATABASE_URL = f"{DB['ENGINE']}://{DB['USER']}:{DB['PASSWORD']}@{DB['HOST']}:{DB['PORT']}/{DB['NAME']}"
DATABASE_TEST_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


test_engine = create_engine(DATABASE_TEST_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


def get_test_session():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
