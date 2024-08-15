from datetime import date, datetime

from config import Base
from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20))

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")
    customers = relationship("Customer", back_populates="sales_contact")
    events = relationship("Event", back_populates="support_contact")


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50), index=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    company_name = Column(String(70), nullable=False)
    creation_date = Column(Date, default=date.today(), nullable=False)
    last_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    sales_contact_id = Column(Integer, ForeignKey("users.id"))

    sales_contact = relationship("User", back_populates="customers")
    contracts = relationship("Contract", back_populates="customer")


class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    amount_total = Column(Float)
    amount_due = Column(Float)
    creation_date = Column(Date, default=date.today())
    is_signed = Column(Boolean, nullable=False, default=False)

    customer = relationship("Customer", back_populates="contracts")
    event = relationship("Event", back_populates="contract")


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(100), index=True, nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    event_start_date = Column(DateTime)
    event_end_date = Column(DateTime)
    support_contact_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String(200))
    attendees = Column(Integer)
    notes = Column(String(255))

    contract = relationship("Contract", back_populates="event")
    support_contact = relationship("User", back_populates="events")
