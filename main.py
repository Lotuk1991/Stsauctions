# main.py
from aiogram import executor
from bot import dp
import handlers_lot  # <-- обязательно
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
