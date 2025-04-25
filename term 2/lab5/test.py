from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio

TOKEN = "7612718600:AAFJloW4OOjdWIkvL8vXNZ-0aR-LVJq4FT8"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик сердечка
@dp.message(F.text.in_({'❤️', '🧡', '💛', '💚', '💙', '💜'}))
async def send_colored_kiss(message: types.Message):
    color_map = {
        '❤️': 'красным',
        '🧡': 'оранжевым',
        '💛': 'жёлтым',
        '💚': 'зелёным',
        '💙': 'голубым',
        '💜': 'фиолетовым'
    }
    await message.answer(f"💋{message.text} Вот тебе поцелуй с {color_map[message.text]} сердечком!")
@dp.message(F.text == '05.09.2024')
async def send_kiss(message: types.Message):
    responses = [
        "💋❤️ Вот тебе поцелуйчик!",
        "💋❤️ Возвращаю сердечко с поцелуем!",
        "💋❤️ Ммм-чмок!",
        "💋❤️ Лови поцелуйчик, солнышко!"
    ]
    import random
    await message.answer(random.choice(responses))

# Стандартные команды
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Отправь мне ❤️ и получишь поцелуй в ответ!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())