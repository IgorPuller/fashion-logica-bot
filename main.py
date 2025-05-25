from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
import requests
from handlers import start, handle_button, handle_user_text, handle_photo


# Загрузка переменных из .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Команды и кнопки
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Начать заново$"), start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Текст — идёт в GPT
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_text))

    print("Бот запущен...")
    app.run_polling()





