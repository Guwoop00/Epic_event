from datetime import date, datetime
from config import Base
from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship


class Role(Base):
    __tablename__ = "roles"
    id: int = Column(Integer, primary_key=True, nullable=False)
    name: str = Column(String(20))

    users = relationship("User", back_populates="role")

    """Represents a role that can be assigned to users."""


class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, index=True)
    full_name: str = Column(String(50), unique=True, nullable=False)
    email: str = Column(String(50), unique=True, nullable=False)
    password: str = Column(String(200), nullable=False)
    role_id: int = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")
    customers = relationship("Customer", back_populates="sales_contact")
    events = relationship("Event", back_populates="support_contact")

    """Represents a user in the system, with a role and related customers/events."""


class Customer(Base):
    __tablename__ = "customers"
    id: int = Column(Integer, primary_key=True, index=True)
    full_name: str = Column(String(50), index=True, nullable=False)
    email: str = Column(String(100), nullable=False, unique=True)
    phone: str = Column(String(20), nullable=False, unique=True)
    company_name: str = Column(String(70), nullable=False)
    creation_date: date = Column(Date, default=date.today(), nullable=False)
    last_update: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    sales_contact_id: int = Column(Integer, ForeignKey("users.id"))

    sales_contact = relationship("User", back_populates="customers")
    contracts = relationship("Contract", back_populates="customer")

    """Represents a customer with contact details and associated contracts."""


class Contract(Base):
    __tablename__ = "contracts"
    id: int = Column(Integer, primary_key=True, index=True)
    customer_id: int = Column(Integer, ForeignKey("customers.id"))
    amount_total: float = Column(Float)
    amount_due: float = Column(Float)
    creation_date: date = Column(Date, default=date.today())
    is_signed: bool = Column(Boolean, nullable=False, default=False)

    customer = relationship("Customer", back_populates="contracts")
    event = relationship("Event", back_populates="contract")

    """Represents a contract with financial details and associated event."""


class Event(Base):
    __tablename__ = "events"
    id: int = Column(Integer, primary_key=True, index=True)
    event_name: str = Column(String(100), index=True, nullable=False)
    contract_id: int = Column(Integer, ForeignKey("contracts.id"))
    event_start_date: datetime = Column(DateTime)
    event_end_date: datetime = Column(DateTime)
    support_contact_id: int = Column(Integer, ForeignKey("users.id"))
    location: str = Column(String(200))
    attendees: int = Column(Integer)
    notes: str = Column(String(255))

    contract = relationship("Contract", back_populates="event")
    support_contact = relationship("User", back_populates="events")

    """Represents an event with details, including dates, location, and associated contract."""
