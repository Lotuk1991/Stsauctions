from aiogram import types, Dispatcher
from copart_lot_parser import get_lot_info

async def lot_handler(message: types.Message):
    args = message.get_args()
    if not args or not args.isdigit():
        await message.reply("Будь ласка, введи номер лота. Наприклад:\n/lot 47901355")
        return

    lot_number = args.strip()
    await message.answer(f"🔍 Шукаю інформацію по лоту `{lot_number}`...")

    try:
        info = await get_lot_info(lot_number)
        text = (
            f"🚗 **{info['title']}**\n"
            f"📍 Місце продажу: *{info['location']}*\n"
            f"🔋 Двигун: {info['engine']}\n"
            f"⛽️ Паливо: {info['fuel']}\n"
            f"📄 Документ: {info['doc_type']}\n"
            f"🔑 VIN: `{info['vin']}`\n"
            f"\n🔗 [Переглянути лот]({info['url']})"
        )
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer("⚠️ Не вдалося отримати дані. Спробуйте пізніше.")
        print(f"LOT ERROR: {e}")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(lot_handler, commands=["lot"])
