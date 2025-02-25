from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from aiogram import Bot
from db import get_db  
from bot import BOT_TOKEN

app = FastAPI()

API_TOKEN = BOT_TOKEN
bot = Bot(token=API_TOKEN)

@app.get("/")
async def read_root():
    return {"message": "Hello, this is your bot's admin interface"}

@app.get("/send_message/")
async def send_message(user_id: int, message: str):
    # Відправка повідомлення користувачу через бот
    try:
        await bot.send_message(user_id, message)
        return {"status": "Message sent successfully"}
    except Exception as e:
        return {"status": f"Failed to send message: {e}"}



