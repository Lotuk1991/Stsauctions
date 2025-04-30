import logging
from aiogram import Bot, Dispatcher, executor, types
from handlers import register_handlers
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

register_handlers(dp)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привіт! Введи команду /copart bmw 3 щоб знайти авто на Copart.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)