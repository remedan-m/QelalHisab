from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from .database import Base

class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String)
    payment_type = Column(String, nullable=False)  # cash or credit

class Expense(Base):
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)
    is_regular = Column(Boolean, default=True)
    payment_type = Column(String, nullable=False)  # cash or credit
