from src.database.db import engine
from src.database.models import Base

# Создание всех таблиц
Base.metadata.create_all(bind=engine)
