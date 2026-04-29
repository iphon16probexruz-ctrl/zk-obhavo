from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.image_generator import create_image

# 🔹 User state
user_data = {}


# 🔘 BACK
def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back"))
    return kb


# ☀️ DAY ICONS
def day_icon_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("☀️ Quyosh", callback_data="day_quyosh"),
        InlineKeyboardButton("🌤 Bulut+Quyosh", callback_data="day_bulutQuyosh"),
        InlineKeyboardButton("🌦 Quyosh+Yomg‘ir", callback_data="day_quyoshYomgir"),
        InlineKeyboardButton("🌨 Bulut+Qor", callback_data="day_bulutQor"),
        InlineKeyboardButton("❄️ Qor", callback_data="day_qor"),
    )
    kb.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back"))
    return kb


# 🌙 NIGHT ICONS
def night_icon_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("❄️ Qor", callback_data="night_qor"),
        InlineKeyboardButton("🌨 Bulut+Qor", callback_data="night_bulutQor"),
        InlineKeyboardButton("🌙 Oy", callback_data="night_oy"),
        InlineKeyboardButton("☁️🌙 Bulut+Oy", callback_data="night_bulutOy"),
        InlineKeyboardButton("🌧🌙 Oy+Yomg‘ir", callback_data="night_oyYomgir"),
    )
    kb.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back"))
    return kb


# ▶️ START
async def start_weather(message: types.Message):
    uid = message.from_user.id
    user_data[uid] = {"step": 1}

    await message.answer("📅 Sanani kiriting:", reply_markup=back_btn())


# 🔄 TEXT STEPS
async def process_weather(message: types.Message):
    uid = message.from_user.id

    if uid not in user_data:
        return

    step = user_data[uid]["step"]

    # 1️⃣ Sana
    if step == 1:
        user_data[uid]["date"] = message.text
        user_data[uid]["step"] = 2
        await message.answer("🌡 Kunduzgi harorat:", reply_markup=back_btn())

    # 2️⃣ Kunduz temp
    elif step == 2:
        user_data[uid]["day_temp"] = message.text
        user_data[uid]["step"] = 3
        await message.answer("🌙 Kechqurun harorat:", reply_markup=back_btn())

    # 3️⃣ Kechki temp
    elif step == 3:
        user_data[uid]["night_temp"] = message.text
        user_data[uid]["step"] = 4
        await message.answer("☀️ Kunduz icon tanlang:", reply_markup=day_icon_keyboard())

    # 6️⃣ Namlik
    elif step == 6:
        user_data[uid]["humidity"] = message.text
        user_data[uid]["step"] = 7
        await message.answer("🌬 Shamol tezligi (m/s):", reply_markup=back_btn())

    # 7️⃣ FINISH
    elif step == 7:
        user_data[uid]["wind"] = message.text

        await message.answer("⏳ Rasm yaratilmoqda...")

        buffer = create_image(user_data[uid])
        await message.answer_photo(buffer)

        del user_data[uid]


# 🔘 CALLBACKS
async def weather_callbacks(call: types.CallbackQuery):
    uid = call.from_user.id

    if uid not in user_data:
        await call.answer()
        return

    step = user_data[uid]["step"]

    # 🔙 BACK
    if call.data == "back":
        user_data[uid]["step"] = max(1, step - 1)
        step = user_data[uid]["step"]

        if step == 1:
            await call.message.edit_text("📅 Sanani kiriting:", reply_markup=back_btn())

        elif step == 2:
            await call.message.edit_text("🌡 Kunduzgi harorat:", reply_markup=back_btn())

        elif step == 3:
            await call.message.edit_text("🌙 Kechqurun harorat:", reply_markup=back_btn())

        elif step == 4:
            await call.message.edit_text("☀️ Kunduz icon tanlang:", reply_markup=day_icon_keyboard())

        elif step == 5:
            await call.message.edit_text("🌙 Kechqurun icon tanlang:", reply_markup=night_icon_keyboard())

        elif step == 6:
            await call.message.edit_text("💧 Namlik (%):", reply_markup=back_btn())

        await call.answer()
        return

    # ☀️ DAY ICON
    if step == 4 and call.data.startswith("day_"):
        user_data[uid]["day_icon"] = call.data.replace("day_", "")
        user_data[uid]["step"] = 5

        await call.message.edit_text("🌙 Kechqurun icon tanlang:", reply_markup=night_icon_keyboard())

    # 🌙 NIGHT ICON
    elif step == 5 and call.data.startswith("night_"):
        user_data[uid]["night_icon"] = call.data.replace("night_", "")
        user_data[uid]["step"] = 6

        await call.message.edit_text("💧 Namlik (%):", reply_markup=back_btn())

    await call.answer()


# 🔗 REGISTER
def register_weather(dp):
    dp.register_message_handler(start_weather, lambda m: m.text == "🌤 Ob-havo rasm yaratish")
    dp.register_message_handler(process_weather)
    dp.register_callback_query_handler(weather_callbacks)