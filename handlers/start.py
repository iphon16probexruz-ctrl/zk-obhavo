from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# 🔘 Asosiy menyu tugmasi
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🌤 Ob-havo rasm yaratish"))
    return kb


# ▶️ /start komandasi
async def start_handler(message: types.Message):
    text = (
        "👋 Assalomu alaykum!\n\n"
        "Bu bot ob-havo ma'lumotlari asosida rasm yaratadi.\n\n"
        "Boshlash uchun pastdagi tugmani bosing 👇"
    )
    await message.answer(text, reply_markup=main_menu())


# 🔗 Register
def register_start(dp):
    dp.register_message_handler(start_handler, commands=["start"])