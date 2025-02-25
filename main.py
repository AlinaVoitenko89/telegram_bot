import uvicorn
import asyncio
from multiprocessing import Process
from bot import start_handler
from admin import app

# Запуск бота та FastAPI разом(одночасно)
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    bot_process = Process(target=asyncio.run, args=(start_handler(),))
    bot_process.start()

    run_fastapi()

    bot_process.join()