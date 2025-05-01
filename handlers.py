# handlers.py

from aiogram import types
from bot import dp
from copart_lot_parser import get_copart_lot_info

@dp.message_handler(commands=["lot"])
async def handle_lot_command(message: types.Message):
    lot_id = message.get_args().strip()
    if not lot_id.isdigit():
        await message.reply("❗️Вкажи номер лота після /lot")
        return

    await message.reply(f"🔍 Шукаю інформацію по лоту {lot_id}...")
    try:
        result = get_copart_lot_info(lot_id)
        await message.reply(result, parse_mode="HTML")
    except Exception as e:
        await message.reply(f"❌ Помилка при отриманні лота: {e}")
