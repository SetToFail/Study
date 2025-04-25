import os
import sqlite3
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from PIL import Image, ImageOps
import aiohttp
import hashlib

# Инициализация бота и планировщика
TOKEN = "7612718600:AAFJloW4OOjdWIkvL8vXNZ-0aR-LVJq4FT8"
WEATHERAPI_KEY = "1e2f733ba8004613a35132921252404"
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# Конфигурация
ADMIN_IDS = [943176374]  # ID администраторов
PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

# 3.1 Аутентификация пользователя
class AuthStates(StatesGroup):
    waiting_for_password = State()

user_sessions = {}

# 3.3 Планировщик напоминаний
class ReminderStates(StatesGroup):
    waiting_for_time = State()
    waiting_for_text = State()

# 3.2 База данных
import sqlite3
from datetime import datetime

# Регистрируем новые адаптеры
def adapt_datetime(dt):
    return dt.isoformat()

def convert_datetime(ts):
    return datetime.fromisoformat(ts.decode())

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("datetime", convert_datetime)

def init_db():
    with sqlite3.connect("bot.db", detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            timestamp DATETIME
        )
        """)
        conn.commit()

def log_action(user_id: int, action: str):
    with sqlite3.connect("bot.db", detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_actions (user_id, action, timestamp) VALUES (?, ?, ?)",
            (user_id, action, datetime.now())
        )
        conn.commit()

@dp.message(Command("history"))
async def get_history(message: types.Message):
    with sqlite3.connect("bot.db", detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT action, timestamp FROM user_actions WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10",
            (message.from_user.id,)
        )
        actions = cursor.fetchall()
    
    if not actions:
        return await message.answer("История действий пуста")
    
    history = ["📆 Ваша история действий:"]
    for i, (action, timestamp) in enumerate(actions, 1):
        history.append(f"{i}. {action} - {timestamp.strftime('%d.%m.%Y %H:%M')}")
    
    await message.answer("\n".join(history))

# 3.1 Аутентификация
@dp.message(Command("auth"))
async def start_auth(message: Message, state: FSMContext):
    await state.set_state(AuthStates.waiting_for_password)
    await message.answer("Введите пароль для доступа к привилегированным командам:")

@dp.message(AuthStates.waiting_for_password)
async def check_password(message: Message, state: FSMContext):
    input_hash = hashlib.sha256(message.text.encode()).hexdigest()
    if input_hash == PASSWORD_HASH:
        user_sessions[message.from_user.id] = True
        await message.answer("✅ Авторизация успешна!")
    else:
        await message.answer("❌ Неверный пароль!")
    await state.clear()

# 3.3 Напоминания
@dp.message(Command("remind"))
async def start_reminder(message: Message, state: FSMContext):
    await state.set_state(ReminderStates.waiting_for_time)
    await message.answer("На когда установить напоминание? (Формат: DD.MM.YYYY HH:MM)")

@dp.message(ReminderStates.waiting_for_time)
async def set_reminder_time(message: Message, state: FSMContext):
    try:
        reminder_time = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        await state.update_data(reminder_time=reminder_time)
        await state.set_state(ReminderStates.waiting_for_text)
        await message.answer("Введите текст напоминания:")
    except ValueError:
        await message.answer("Неправильный формат даты. Используйте DD.MM.YYYY HH:MM")

@dp.message(ReminderStates.waiting_for_text)
async def set_reminder_text(message: Message, state: FSMContext):
    data = await state.get_data()
    scheduler.add_job(
        send_reminder,
        "date",
        run_date=data["reminder_time"],
        args=(message.from_user.id, message.text),
        id=f"reminder_{message.from_user.id}_{datetime.now().timestamp()}"
    )
    await message.answer(f"⏰ Напоминание установлено на {data['reminder_time'].strftime('%d.%m.%Y %H:%M')}")
    await state.clear()

async def send_reminder(user_id: int, text: str):
    await bot.send_message(user_id, f"🔔 Напоминание: {text}")

# 3.5 Погода (WeatherAPI)
@dp.message(Command("weather"))
async def get_weather(message: Message):
    city = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    
    if not city:
        await message.answer("Укажите город: /weather <город>")
        return
    
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={city}&lang=ru"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                
                weather_info = (
                    f"🌦 Погода в {data['location']['name']}:\n"
                    f"🌡 Температура: {data['current']['temp_c']}°C\n"
                    f"💧 Влажность: {data['current']['humidity']}%\n"
                    f"🌬 Ветер: {data['current']['wind_kph']} км/ч\n"
                    f"☁ {data['current']['condition']['text']}"
                )
                await message.answer(weather_info)
                log_action(message.from_user.id, f"Запрос погоды для {city}")
                
    except Exception as e:
        await message.answer("Не удалось получить погоду. Попробуйте позже.")
        print(f"Ошибка WeatherAPI: {e}")

# 3.4 Обработка фото
@dp.message(Command("bw"))
async def request_photo(message: Message):
    await message.answer("Отправьте фото для конвертации в чёрно-белое:")

@dp.message(F.photo)
async def process_photo(message: Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    download_path = f"downloads/{photo.file_id}.jpg"
    os.makedirs("downloads", exist_ok=True)
    await bot.download_file(file.file_path, download_path)
    
    # Асинхронная обработка
    await process_image_async(download_path, message.from_user.id)
    log_action(message.from_user.id, "Обработано фото в ЧБ")

async def process_image_async(path: str, user_id: int):
    def sync_processing():
        with Image.open(path) as img:
            bw_img = ImageOps.grayscale(img)
            bw_path = path.replace(".jpg", "_bw.jpg")
            bw_img.save(bw_path)
            return bw_path
    
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    
    with ThreadPoolExecutor() as pool:
        bw_path = await asyncio.get_event_loop().run_in_executor(pool, sync_processing)
    
    await bot.send_photo(user_id, FSInputFile(bw_path))
    os.remove(path)
    os.remove(bw_path)

# 3.6 Админ-панель
@dp.message(Command("stats"))
async def show_stats(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("🚫 Доступ запрещен")
    
    with sqlite3.connect("bot.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM user_actions")
        users_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM user_actions")
        actions_count = cursor.fetchone()[0]
    
    await message.answer(
        f"📊 Статистика:\nУникальных пользователей: {users_count}\nВсего действий: {actions_count}"
    )

# Запуск бота
async def main():
    init_db()
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())