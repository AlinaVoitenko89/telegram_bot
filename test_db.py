from db import get_db
from sqlalchemy import text
import asyncio

async def test_db():
    try:
        async for session in get_db():
            result = await session.execute(text("SELECT 1"))
            print(f"Рузультат запиту: {result.scalar()}")
    except Exception as e:
        print(f"Помилка підключення до БД: {e}")

if __name__ == "__main__":
    asyncio.run(test_db())
