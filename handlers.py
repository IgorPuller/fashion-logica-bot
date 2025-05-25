from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from yandex_gpt import ask_yandex_gpt
from fashionclip_handler import process_photo
import os

# Reply-клавиатура внизу
reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Начать заново")]],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Главное меню
inline_keyboard_start = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("👗 ИИ стилист", callback_data="choose_ai"),
        InlineKeyboardButton("💬 Живой человек", url="https://t.me/igorpuller")
    ]
])

# Подменю ИИ стилиста
inline_keyboard_ai = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📸 Загрузить фото", callback_data="upload_photo"),
        InlineKeyboardButton("💬 Задать вопрос", callback_data="ask_ai")
    ],
    [
        InlineKeyboardButton("🔙 Назад", callback_data="back_to_start")
    ]
])

# Кнопки после загрузки фото
inline_keyboard_after_photo = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("➕ Добавить ещё фото", callback_data="more_photos"),
        InlineKeyboardButton("🤖 Получить ответ от ИИ", callback_data="analyze_photos")
    ]
])


# /start или "Начать заново"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Очистка загруженных фото
    for path in context.user_data.get("photos", []):
        if os.path.exists(path):
            os.remove(path)
    context.user_data.clear()

    await update.message.reply_text(
        "Привет! Я бот-стилист 👗",
        reply_markup=reply_keyboard
    )
    await update.message.reply_text(
        "Кто тебе поможет?",
        reply_markup=inline_keyboard_start
    )


# Inline-кнопки
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "choose_ai":
        await query.edit_message_text(
            "Ты выбрал ИИ стилиста 🤖. Что хочешь сделать?",
            reply_markup=inline_keyboard_ai
        )

    elif query.data == "upload_photo":
        await query.edit_message_text("Пришли мне фото одежды, которую хочешь проанализировать 📸")

    elif query.data == "ask_ai":
        await query.edit_message_text("Опиши, что тебе нужно 👇")

    elif query.data == "back_to_start":
        await query.edit_message_text(
            "Кто тебе поможет?",
            reply_markup=inline_keyboard_start
        )

    elif query.data == "more_photos":
        await query.edit_message_text("Пришли следующее фото 📸")

    elif query.data == "analyze_photos":
        photos = context.user_data.get("photos", [])
        if not photos:
            await query.edit_message_text("⚠️ Сначала пришли хотя бы одно фото.")
            return

        await query.edit_message_text("🧠 Анализирую образ... Подожди немного 👗")

        try:
            results = [process_photo(p) for p in photos]
            combined_result = "\n".join(f"{i+1}) {r}" for i, r in enumerate(results))

            await context.bot.send_message(
                chat_id=query.message.chat.id,
                text=f"Вот, что я думаю:\n{combined_result}",
                reply_markup=reply_keyboard
            )
        except Exception as e:
            await context.bot.send_message(
                chat_id=query.message.chat.id,
                text="⚠️ Ошибка при анализе изображения."
            )
            print("FashionCLIP error:", e)

        for path in photos:
            if os.path.exists(path):
                os.remove(path)
        context.user_data.clear()


# Текст: вопрос к GPT или "Начать заново"
async def handle_user_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    if text == "начать заново":
        await start(update, context)
        return

    try:
        response = ask_yandex_gpt(update.message.text)
        await update.message.reply_text(response, reply_markup=reply_keyboard)
    except Exception as e:
        await update.message.reply_text("⚠️ Ошибка при обращении к ИИ.")
        print("YandexGPT error:", e)


# Фото: сохраняем и предлагаем следующее действие
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_photos = context.user_data.setdefault("photos", [])

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = f"temp_photo_{update.message.from_user.id}_{len(user_photos)}.jpg"
    await file.download_to_drive(file_path)

    user_photos.append(file_path)

    await update.message.reply_text(
        f"📸 Фото {len(user_photos)} сохранено.",
        reply_markup=inline_keyboard_after_photo
    )


