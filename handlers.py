from aiogram import types
from copart_lot_parser import get_lot_info

async def lot_handler(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("Введи номер лота. Наприклад:\n/lot 47813034")
        return

    lot_number = args.strip()
    await message.answer(f"Шукаю інформацію по лоту {lot_number}...")

    try:
        info = await get_lot_info(lot_number)
        response = (
            f"**{info['title']}**\n"
            f"Місцезнаходження: {info['location']}\n"
            f"VIN: `{info['vin']}`\n"
            f"[Посилання на лот]({info['url']})"
        )
        await message.answer(response, parse_mode="Markdown")
    except Exception as e:
        await message.answer("Сталася помилка під час пошуку. Спробуйте пізніше.")
        print(e)