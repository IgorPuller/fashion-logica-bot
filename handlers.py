from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from yandex_gpt import ask_yandex_gpt
import os

reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Начать заново")]],
    resize_keyboard=True,
    one_time_keyboard=False
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-стилист 👗",
        reply_markup=reply_keyboard
    )
    await update.message.reply_text(
        "Кто тебе поможет?",
        reply_markup=inline_keyboard
    )

inline_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("👗 ИИ стилист", callback_data="ai_stylist")],
    [InlineKeyboardButton("📸 Загрузить фото", callback_data="upload_photo")],
    [InlineKeyboardButton("💬 Живой человек", url="https://t.me/igorpuller")]
])

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ai_stylist":
        await query.edit_message_text("Выбран ИИ стилист. Опиши, что тебе нужно 👇")
        #await query.edit_message_text("Выбран ИИ стилист. Опиши, что тебе нужно 👇", reply_markup=ForceReply())
    elif query.data == "upload_photo":
        await query.edit_message_text("Пришли мне фото одежды, которую хочешь проанализировать 📸")


# Обработка текстовых сообщений — вызов GPT
async def handle_user_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    #await update.message.reply_text("Подумаю над твоим образом... 👗")

    try:
        response = ask_yandex_gpt(prompt)
        #await update.message.reply_text(response)
        await update.message.reply_text(response, reply_markup=reply_keyboard)
    except Exception as e:
        await update.message.reply_text("⚠️ Ошибка при обращении к ИИ.")
        print("YandexGPT error:", e)

from fashionclip_handler import process_photo

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = f"temp_photo_{update.message.from_user.id}.jpg"
    await file.download_to_drive(file_path)

    try:
        result = process_photo(file_path)
        await update.message.reply_text(f"🧠 Вот что я думаю:\n{result}")
    except Exception as e:
        await update.message.reply_text("⚠️ Ошибка при анализе изображения.")
        print("FashionCLIP error:", e)

    os.remove(file_path)
