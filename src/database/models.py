from sqlalchemy import Column, Integer, BigInteger, String,ForeignKey
from src.database.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)


