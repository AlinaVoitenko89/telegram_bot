from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy.future import select
from models import User, Base
import asyncio

# Завантаження змінних середовища з .env
load_dotenv()

DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_USER=os.getenv("DB_USER")
DB_NAME=os.getenv("DB_NAME")
DB_PASSWORD=os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(DATABASE_URL)

# Перевіряємо, чи коректно завантажилась змінна
if not DATABASE_URL:
    raise ValueError("DATABASE_URL не знайдено в .env файлі")

# Створюємо асинхронний двигун SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика для створення асинхронних сесій
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Функція для отримання сесії
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Функція для запису нового користувача у БД
async def add_user(session: AsyncSession, telegram_id: int, username: str, full_name: str):
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalars().first()

    if not user:
        new_user = User(telegram_id=telegram_id, username=username, full_name=full_name)
        session.add(new_user)
        await session.commit()