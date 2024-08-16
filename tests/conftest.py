import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controllers.user_controller import UserController
from controllers.event_controller import EventController
from controllers.customer_controller import CustomerController
from controllers.contract_controller import ContractController
from utils.validators import DataValidator
from models.models import Base, Role, User, Event, Customer, Contract
from utils.jwtoken import TokenManager

DATABASE_TEST_URL = "sqlite:///:memory:"
test_engine = create_engine(DATABASE_TEST_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    # Cleanup code after each test
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def session():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def user_controller(session, mocker):
    user_controller = UserController(session=session)
    user_controller.token_manager = TokenManager()
    user_controller.user_view = mocker.MagicMock()
    user_controller.validators = mocker.MagicMock()
    return user_controller


@pytest.fixture
def event_controller(session, mocker):
    controller = EventController(session=session)
    controller.token_manager = TokenManager()
    controller.event_view = mocker.MagicMock()
    controller.validators = mocker.MagicMock()
    return controller


@pytest.fixture
def customer_controller(session, mocker):
    controller = CustomerController(session=session)
    controller.token_manager = TokenManager()
    controller.customer_view = mocker.MagicMock()
    controller.validators = mocker.MagicMock()
    return controller


@pytest.fixture
def contract_controller(session, mocker):
    controller = ContractController(session=session)
    controller.token_manager = TokenManager()
    controller.contract_view = mocker.MagicMock()
    controller.validators = mocker.MagicMock()
    return controller


@pytest.fixture
def validator(session):
    """Fixture pour fournir une instance de DataValidator avec une session mockée"""
    return DataValidator(session=session)


@pytest.fixture
def token_manager():
    """Fixture pour initialiser une instance de TokenManager."""
    return TokenManager()


@pytest.fixture
def mock_user():
    """Fixture pour créer un utilisateur mock."""
    role = Role(id=1, name='admin')
    user = User(id=1, email='test@example.com', full_name='Test User', password='hashed_password', role=role)
    return user


@pytest.fixture
def create_authenticated_user(session, user_controller):
    def _create_authenticated_user(user_id=1, email="auth@ex.com", full_name="Auth User",
                                   password='Azerty13', role_name="UserRole"):
        hashed_password = user_controller.hash_password(password)
        role = Role(id=1, name=role_name)
        authenticated_user = User(id=user_id, email=email, full_name=full_name, password=hashed_password, role=role)
        session.add(role)
        session.add(authenticated_user)
        session.commit()
        return authenticated_user
    return _create_authenticated_user


@pytest.fixture
def create_mock_user(session):
    def _create_mock_user(user_id=1, email="test@example.com", full_name="Test User", password="hashed_password"):
        mock_user = User(id=user_id, email=email, full_name=full_name, password=password)
        session.add(mock_user)
        session.commit()
        return mock_user
    return _create_mock_user


@pytest.fixture
def create_mock_event(session):
    def _create_mock_event(event_name="Default Event", contract_id=1, event_start_date=date.today(),
                           event_end_date=date.today(), location="Default Location",
                           attendees=10, notes="Default Notes"):
        event = Event(event_name=event_name, contract_id=contract_id, event_start_date=event_start_date,
                      event_end_date=event_end_date, location=location, attendees=attendees, notes=notes)
        session.add(event)
        session.commit()
        return event
    return _create_mock_event


@pytest.fixture
def create_mock_customer(session):
    def _create_mock_customer(full_name="John Doe", email="john.doe@example.com",
                              phone="1234567890", company_name="Doe Inc."):
        customer = Customer(full_name=full_name, email=email, phone=phone, company_name=company_name)
        session.add(customer)
        session.commit()
        return customer
    return _create_mock_customer


@pytest.fixture
def create_contract(session):
    def _create_contract(customer_id=1, amount_total=1000.0, amount_due=500.0, is_signed=False):
        contract = Contract(customer_id=customer_id, amount_total=amount_total,
                            amount_due=amount_due, is_signed=is_signed)
        session.add(contract)
        session.commit()
        return contract
    return _create_contract


@pytest.fixture
def test_login_required(mocker):
    mocker.patch.object(TokenManager, 'get_tokens', return_value="fake_access_token")
    mocker.patch.object(TokenManager, 'check_token', return_value=True)
    mocker.patch.object(TokenManager, 'validate_token', return_value=True)
