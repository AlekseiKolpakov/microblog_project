from sqlalchemy import Column, Integer, String

from backend.core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
