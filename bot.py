from aiogram import Bot, Dispatcher, executor
import logging

from config import TOKEN
from handlers.start import register_start
from handlers.weather import register_weather

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def register_all(dp):
    register_start(dp)
    register_weather(dp)


if __name__ == "__main__":
    register_all(dp)
    print("🚀 PSG Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)