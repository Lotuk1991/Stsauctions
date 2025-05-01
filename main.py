import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from handlers import register_handlers
register_handlers(dp)


# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота і диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Реєстрація хендлера
dp.register_message_handler(lot_handler, commands=["lot"])

# Обробник команди /start
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Привіт! Введи команду /lot 47813034 щоб знайти авто на Copart.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
