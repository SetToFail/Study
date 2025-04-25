import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from pathlib import Path
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler
)

# cfg
TOKEN = "7612718600:AAFJloW4OOjdWIkvL8vXNZ-0aR-LVJq4FT8"
BASE_DIR = Path(__file__).parent
PHOTO_PATH = BASE_DIR / "images" / "bot_image.jpg"

# 1.1 Эхо-бот + 1.2 Приветственный бот
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"""
    👋 Привет, {user.first_name}! Я многофункциональный бот.

    📌 Доступные команды:
    /start - Начальное меню
    /help - Список всех команд
    /photo - Получить тестовое фото
    /menu - Интерактивное меню

    Просто отправь мне текст, и я его повторю!
    """
    await update.message.reply_text(welcome_text)

# 1.1 Эхо-бот
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# 1.3 Бот-команды
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    🆘 Справка по командам:

    /start - Главное меню с приветствием
    /help - Эта справка
    /photo - Получить тестовое изображение
    /menu - Открыть интерактивное меню

    ℹ Просто отправьте текст - бот его повторит
    """
    await update.message.reply_text(help_text)

# 1.4 Фотоотправитель
async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(PHOTO_PATH):
        await update.message.reply_text("Фото не найдено!")
        return

    caption = "Вот тестовое изображение из локальной папки 📁"
    with open(PHOTO_PATH, 'rb') as photo:
        await update.message.reply_photo(photo, caption=caption)

# 1.5 Бот с кнопками
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Команда 1", callback_data="1"),
            InlineKeyboardButton("Команда 2", callback_data="2")
        ],
        [
            InlineKeyboardButton("О боте", callback_data="about"),
            InlineKeyboardButton("Закрыть", callback_data="close")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "1":
        await query.edit_message_text("Выбрана команда 1 ✅")
    elif query.data == "2":
        await query.edit_message_text("Выбрана команда 2 ✅")
    elif query.data == "about":
        await query.edit_message_text("Это тестовый бот с inline-кнопками")
    elif query.data == "close":
        await query.delete_message()

def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))  # 1.1 + 1.2
    application.add_handler(CommandHandler("help", help_command))  # 1.3
    application.add_handler(CommandHandler("photo", send_photo))  # 1.4
    application.add_handler(CommandHandler("menu", show_menu))  # 1.5
    
    # Обработчик текстовых сообщений (1.1)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Обработчик inline-кнопок (1.5)
    application.add_handler(CallbackQueryHandler(button_handler))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()