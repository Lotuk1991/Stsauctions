# handlers.py
from aiogram import types
from bot import dp
from copart_lot_parser import get_lot_info

@dp.message_handler(commands=["lot"])
async def handle_lot(message: types.Message):
    lot_id = message.get_args().strip()
    if not lot_id.isdigit():
        await message.reply("Вкажи номер лота, наприклад: /lot 47295215")
        return

    await message.reply("🔍 Шукаю інформацію...")
    result = get_lot_info(lot_id)
    await message.reply(result, parse_mode="HTML")
