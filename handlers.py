from aiogram import types, Dispatcher
from copart_lot_parser import get_lot_info

async def lot_handler(message: types.Message):
    args = message.get_args()
    if not args or not args.isdigit():
        await message.reply("Будь ласка, введи номер лота. Наприклад:\n/lot 49490485")
        return

    lot_number = args.strip()
    await message.answer(f"🔍 Шукаю інформацію по лоту `{lot_number}`...")

    try:
        info = await get_lot_info(lot_number)

        if "error" in info:
            await message.answer(
                f"⚠️ {info['error']}\n🔗 [Переглянути лот]({info.get('url', '')})",
                parse_mode="Markdown"
            )
            return

        text = (
            f"🚗 **{info.get('title', '-') or '-'}**\n"
            f"📍 Місце продажу: *{info.get('location', '-') or '-'}*\n"
            f"🛠️ Двигун: {info.get('engine', '-') or '-'}\n"
            f"⛽ Паливо: {info.get('fuel', '-') or '-'}\n"
            f"📄 Документ: {info.get('doc_type', '-') or '-'}\n"
            f"🔍 VIN: `{info.get('vin', '-') or '-'}`\n\n"
            f"🔗 [Переглянути лот]({info.get('url', '')})"
        )

        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        print(f"LOT ERROR: {e}")
        await message.answer("❌ Помилка при отриманні лота. Спробуйте пізніше.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(lot_handler, commands=["lot"])