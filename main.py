
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from handlers import register_handlers

bot = Bot(token=8034179968:AAEKuR_OdrW_T2BKARp2i0FnKRKXSWXazdQ)
dp = Dispatcher(bot)

register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
