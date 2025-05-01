import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from handlers import lot_handler  # вот этот импорт обязателен!

# Логирование
logging.basicConfig(level=logging.INFO)

# Бот и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Регистрация хендлера /lot
dp.register_message_handler(lot_handler, commands=["lot"])

# Обработчик /start
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Привіт! Введи команду /lot 47813034 щоб знайти авто на Copart.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
