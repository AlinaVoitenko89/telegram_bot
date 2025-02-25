import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import get_db, add_user
from models import User

# Завантажуємо змінні з .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ініціалізуємо бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда start
@dp.message(Command("start"))
async def start_handler(message: Message):
    async for session in get_db():
        await add_user(session, message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.answer("Привіт! Це Telegram-бот!\nНапиши /help, щоб дізнатися, що я вмію.")
        
# Команда /help
@dp.message(Command("help"))
async def help_handler(message: Message):
    commands = """
    ✅ Доступні команди:
    /start - Почати роботу
    /help - Список команд
    /about - Про бота
    /echo <текст> - Повторює твій текст
    """
    await message.answer(commands)

# Команда /about
@dp.message(Command("about"))
async def about_handler(message: Message):
    await message.answer("🤖 Я мінімальний Telegram-бот, написаний на aiogram 3.x + FastAPI.")

# Команда /echo
@dp.message(Command("echo"))
async def echo_handler(message: Message):
    text = message.text.replace("/echo", "").strip()
    if text:
        await message.answer(f"🔄 {text}")
    else:
        await message.answer("❗️ Введи текст після команди /echo.")

async def main():
    print("Бот запущено!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try: 
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот зупинено.")