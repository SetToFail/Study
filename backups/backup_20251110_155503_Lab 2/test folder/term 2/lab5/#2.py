import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from collections import defaultdict

# Инициализация бота
TOKEN = Bot(token="Сокрытие TOKEN")
dp = Dispatcher()

# 2.1 Регистрация пользователей (FSM)
class Registration(StatesGroup):
    name = State()
    email = State()
    confirm = State()

users_data = {}

@dp.message(Command("register"))
async def start_registration(message: types.Message, state: FSMContext):
    await state.set_state(Registration.name)
    await message.answer("Введите ваше имя:")

@dp.message(Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registration.email)
    await message.answer("Теперь введите ваш email:")

@dp.message(Registration.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(Registration.confirm)
    data = await state.get_data()
    await message.answer(
        f"Проверьте данные:\nИмя: {data['name']}\nEmail: {data['email']}\n\nПодтверждаете?",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]
            ],
            resize_keyboard=True
        )
    )

@dp.message(Registration.confirm, F.text.casefold() == "да")
async def process_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    users_data[message.from_user.id] = data
    await message.answer("Регистрация завершена!", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

@dp.message(Registration.confirm, F.text.casefold() == "нет")
async def process_cancel(message: types.Message, state: FSMContext):
    await message.answer("Регистрация отменена", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

# 2.2 Многоуровневое меню
@dp.message(Command("menu"))
async def show_main_menu(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Раздел 1",
        callback_data="section_1")
    )
    builder.add(types.InlineKeyboardButton(
        text="Раздел 2",
        callback_data="section_2")
    )
    await message.answer("Главное меню:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("section_"))
async def process_section(callback: types.CallbackQuery):
    section = callback.data.split("_")[1]
    builder = InlineKeyboardBuilder()
    
    if section == "1":
        builder.add(types.InlineKeyboardButton(
            text="Опция 1.1",
            callback_data="option_1_1")
        )
        builder.add(types.InlineKeyboardButton(
            text="Опция 1.2",
            callback_data="option_1_2")
        )
    elif section == "2":
        builder.add(types.InlineKeyboardButton(
            text="Опция 2.1",
            callback_data="option_2_1")
        )
        builder.add(types.InlineKeyboardButton(
            text="Опция 2.2",
            callback_data="option_2_2")
        )
    
    builder.row(types.InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_main")
    )
    
    await callback.message.edit_text(f"Раздел {section}", reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(F.data.startswith("option_"))
async def process_option(callback: types.CallbackQuery):
    option = callback.data
    await callback.answer(f"Вы выбрали {option.replace('_', ' ')}", show_alert=True)

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await show_main_menu(callback.message)
    await callback.answer()

# 2.3 Обработка геолокации
@dp.message(Command("location"))
async def request_location(message: types.Message):
    await message.answer(
        "Пожалуйста, отправьте ваше местоположение:",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="Отправить местоположение", request_location=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

@dp.message(F.location)
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    await message.answer(
        f"Ваши координаты:\nШирота: {lat}\nДолгота: {lon}",
        reply_markup=types.ReplyKeyboardRemove()
    )

# 2.4 Голосование
votes = defaultdict(int)
poll_options = ["Вариант 1", "Вариант 2", "Вариант 3"]

@dp.message(Command("poll"))
async def create_poll(message: types.Message):
    builder = InlineKeyboardBuilder()
    for idx, option in enumerate(poll_options, 1):
        builder.add(types.InlineKeyboardButton(
            text=f"{option} ({votes[idx]})",
            callback_data=f"vote_{idx}")
        )
    await message.answer("Выберите вариант:", reply_markup=builder.as_markup())
    
@dp.message(Command("show_users"))
async def show_registered_users(message: types.Message):
    if not users_data:
        await message.answer("Нет зарегистрированных пользователей.")
        return
    
    response = "Зарегистрированные пользователи:\n"
    for user_id, data in users_data.items():
        response += f"ID: {user_id}\nИмя: {data['name']}\nEmail: {data['email']}\n\n"
    
    await message.answer(response)

@dp.callback_query(F.data.startswith("vote_"))
async def process_vote(callback: types.CallbackQuery):
    option = int(callback.data.split("_")[1])
    votes[option] += 1
    
    builder = InlineKeyboardBuilder()
    for idx, opt in enumerate(poll_options, 1):
        builder.add(types.InlineKeyboardButton(
            text=f"{opt} ({votes[idx]})",
            callback_data=f"vote_{idx}")
        )
    
    await callback.message.edit_reply_markup(reply_markup=builder.as_markup())
    await callback.answer(f"Вы проголосовали за {poll_options[option-1]}")

# 2.5 Калькулятор
calc_data = {}

@dp.message(Command("calc"))
async def start_calculator(message: types.Message):
    calc_data[message.from_user.id] = {"value": "0", "operation": None, "prev_value": None}
    
    builder = InlineKeyboardBuilder()
    # Первый ряд
    builder.row(
        types.InlineKeyboardButton(text="7", callback_data="calc_7"),
        types.InlineKeyboardButton(text="8", callback_data="calc_8"),
        types.InlineKeyboardButton(text="9", callback_data="calc_9"),
        types.InlineKeyboardButton(text="/", callback_data="calc_/")
    )
    # Второй ряд
    builder.row(
        types.InlineKeyboardButton(text="4", callback_data="calc_4"),
        types.InlineKeyboardButton(text="5", callback_data="calc_5"),
        types.InlineKeyboardButton(text="6", callback_data="calc_6"),
        types.InlineKeyboardButton(text="*", callback_data="calc_*")
    )
    # Третий ряд
    builder.row(
        types.InlineKeyboardButton(text="1", callback_data="calc_1"),
        types.InlineKeyboardButton(text="2", callback_data="calc_2"),
        types.InlineKeyboardButton(text="3", callback_data="calc_3"),
        types.InlineKeyboardButton(text="-", callback_data="calc_-")
    )
    # Четвертый ряд
    builder.row(
        types.InlineKeyboardButton(text="C", callback_data="calc_C"),
        types.InlineKeyboardButton(text="0", callback_data="calc_0"),
        types.InlineKeyboardButton(text="=", callback_data="calc_="),
        types.InlineKeyboardButton(text="+", callback_data="calc_+")
    )
    
    await message.answer(f"Текущее значение: 0", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("calc_"))
async def process_calc_button(callback: types.CallbackQuery):
    button = callback.data.split("_")[1]
    user_data = calc_data.get(callback.from_user.id, {"value": "0"})
    
    if button == "C":
        user_data["value"] = "0"
        user_data["operation"] = None
        user_data["prev_value"] = None
    elif button.isdigit():
        if user_data["value"] == "0":
            user_data["value"] = button
        else:
            user_data["value"] += button
    elif button in ["+", "-", "*", "/"]:
        user_data["prev_value"] = user_data["value"]
        user_data["operation"] = button
        user_data["value"] = "0"
    elif button == "=" and user_data["operation"] and user_data["prev_value"]:
        try:
            expr = f"{user_data['prev_value']} {user_data['operation']} {user_data['value']}"
            result = eval(expr)
            user_data["value"] = str(result)
            user_data["operation"] = None
            user_data["prev_value"] = None
        except:
            user_data["value"] = "Error"
    
    calc_data[callback.from_user.id] = user_data
    
    display_text = user_data["value"]
    if user_data["operation"]:
        display_text = f"{user_data['prev_value']} {user_data['operation']} {user_data['value']}"
    
    # Повторно создаем клавиатуру с тем же расположением
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="7", callback_data="calc_7"),
        types.InlineKeyboardButton(text="8", callback_data="calc_8"),
        types.InlineKeyboardButton(text="9", callback_data="calc_9"),
        types.InlineKeyboardButton(text="/", callback_data="calc_/")
    )
    builder.row(
        types.InlineKeyboardButton(text="4", callback_data="calc_4"),
        types.InlineKeyboardButton(text="5", callback_data="calc_5"),
        types.InlineKeyboardButton(text="6", callback_data="calc_6"),
        types.InlineKeyboardButton(text="*", callback_data="calc_*")
    )
    builder.row(
        types.InlineKeyboardButton(text="1", callback_data="calc_1"),
        types.InlineKeyboardButton(text="2", callback_data="calc_2"),
        types.InlineKeyboardButton(text="3", callback_data="calc_3"),
        types.InlineKeyboardButton(text="-", callback_data="calc_-")
    )
    builder.row(
        types.InlineKeyboardButton(text="C", callback_data="calc_C"),
        types.InlineKeyboardButton(text="0", callback_data="calc_0"),
        types.InlineKeyboardButton(text="=", callback_data="calc_="),
        types.InlineKeyboardButton(text="+", callback_data="calc_+")
    )
    
    await callback.message.edit_text(f"Текущее значение: {display_text}", reply_markup=builder.as_markup())
    await callback.answer()

# 2.6 Обработка текстовых файлов
@dp.message(Command("analyze"))
async def request_file(message: types.Message):
    await message.answer("Пожалуйста, отправьте текстовый файл (TXT) для анализа")

@dp.message(F.document & (F.document.mime_type == "text/plain"))
async def analyze_text_file(message: types.Message):
    file_id = message.document.file_id
    file = await TOKEN.get_file(file_id)
    file_path = file.file_path
    
    download_path = f"downloads/{file_id}.txt"
    os.makedirs("downloads", exist_ok=True)
    
    await TOKEN.download_file(file_path, download_path)
    
    with open(download_path, "r", encoding="utf-8") as f:
        content = f.read()
        words = len(content.split())
        chars = len(content)
        lines = len(content.splitlines())
        
        await message.answer(
            f"Анализ файла:\n"
            f"Слов: {words}\n"
            f"Символов: {chars}\n"
            f"Строк: {lines}"
        )
    
    os.remove(download_path)

# Запуск бота
async def main():
    await dp.start_polling(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
