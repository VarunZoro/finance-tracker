from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    transactions = relationship("Transaction", back_populates="owner")

class Transaction(Base):
    __tablename__ = "transactions"

    id       = Column(Integer, primary_key=True, index=True)
    title    = Column(String, nullable=False)
    amount   = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    type     = Column(String, nullable=False)
    date     = Column(Date, default=datetime.date.today)
    notes    = Column(String, nullable=True)
    user_id  = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="transactions")
