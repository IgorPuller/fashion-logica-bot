from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Клавиатура с inline-кнопками
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("👗 ИИ стилист", callback_data="ai_stylist")],
    [InlineKeyboardButton("💬 Живой человек", url="https://t.me/igorpuller")]  # Замени на нужный юзернейм
])

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-стилист 👗\nКто тебе поможет?",
        reply_markup=keyboard
    )

# Обработка нажатий на inline-кнопки (callback_data)
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ai_stylist":
        await query.edit_message_text("Выбран ИИ стилист. Загружаю моду 🤖...")
        # Тут позже подключим CLIP / YandexGPT

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    print("Бот запущен...")
    app.run_polling()


