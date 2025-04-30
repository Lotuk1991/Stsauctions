
from aiogram import types, Dispatcher
import aiohttp

async def start_handler(message: types.Message):
    await message.answer("Привіт! Введи команду /copart bmw 3 щоб знайти авто на Copart.")

async def copart_handler(message: types.Message):
    query = message.get_args()
    if not query:
        await message.answer("Будь ласка, введи запит. Наприклад: /copart bmw 3")
        return

    url = "https://www.copart.com/public/lots/search"
    params = {"query": query, "size": 5, "page": 0}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()

    results = data.get("data", {}).get("results", [])
    if not results:
        await message.answer("Нічого не знайдено.")
        return

    for lot in results:
        text = f"{lot.get('year')} {lot.get('make')} {lot.get('modelGroup')}
"
        text += f"Статус: {lot.get('saleStatus')}
"
        text += f"Локація: {lot.get('yardName')}
"
        text += f"Роздрібна ціна: ${lot.get('rd', 'N/A')}
"
        text += f"VIN: {lot.get('vin')}
"
        text += f"https://www.copart.com/lot/{lot.get('lotNumberStr')}"
        await message.answer_photo(photo=lot.get("thumbnailImageUrl"), caption=text)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(copart_handler, commands=["copart"])
