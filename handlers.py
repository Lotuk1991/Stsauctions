from aiogram import types, Dispatcher
import aiohttp
from bs4 import BeautifulSoup

async def search_copart(make_model: str):
    url = f"https://www.copart.com/lotSearchResults/?free=true&query={make_model.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "html.parser")
    
    lots = soup.find_all("a", class_="search-result", limit=5)
    results = []

    for lot in lots:
        title = lot.get_text(strip=True)
        link = lot.get("href", "")
        if not link.startswith("http"):
            link = f"https://www.copart.com{link}"
        results.append(f"{title}\n{link}")

    return results if results else ["Нічого не знайдено."]

async def copart_handler(message: types.Message):
    query = message.text.replace("/copart", "").strip()
    if not query:
        await message.reply("Будь ласка, введи запит. Наприклад: /copart bmw 3")
        return

    await message.reply("Шукаємо авто на Copart...")
    results = await search_copart(query)
    await message.reply("\n\n".join(results))

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(copart_handler, commands=["copart"])