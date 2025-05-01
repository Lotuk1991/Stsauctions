# handlers_iaai.py
from aiogram import types
from bot import dp
from iaai_parser import get_iaai_lot_info

@dp.message_handler(commands=["iaai"])
async def handle_iaai_lot(message: types.Message):
    lot_id = message.get_args().strip()
    if not lot_id.isdigit():
        await message.reply("❗️Приклад: /iaai 40896330")
        return

    await message.reply(f"🔍 Шукаю інформацію по лоту `{lot_id}`...", parse_mode="Markdown")
    result = get_iaai_lot_info(lot_id)
    await message.reply(result, parse_mode="HTML")
