from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Указываем путь к файлу базы данных (он создастся автоматически в папке проекта)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2. Создаем движок. Для SQLite обязательно добавляем check_same_thread=False
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Создаем базовый класс для будущих таблиц
Base = declarative_base()
