from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from typing import Any, Dict

Base = declarative_base()

class UserDBModel(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(String, primary_key=True)
    email = Column(String)
    full_name = Column(String)
    password = Column(String)  # text в БД
    created_at = Column(DateTime)  # timestamp в БД
    updated_at = Column(DateTime)  # timestamp в БД
    verified = Column(Boolean)  # bool в БД
    banned = Column(Boolean)  # bool в БД
    roles = Column(String)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            'email': self.email,
            'full_name': self.full_name,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'verified': self.verified,
            'banned': self.banned,
            'roles': self.roles
        }

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}')>"