from sqlalchemy import Column, String,Integer, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from typing import Any, Dict

Base = declarative_base()

class AccountTransactionTemplate(Base):
    __tablename__ = 'accounts_transaction_template'
    user = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)