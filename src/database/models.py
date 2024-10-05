from sqlalchemy import Column, Integer, String
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
