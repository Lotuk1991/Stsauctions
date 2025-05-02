import asyncio
from playwright.async_api import async_playwright

async def get_iaai_full_info(lot_id: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Отримуємо salvageId
        await page.goto(f"https://www.iaai.com/VehicleDetail/{lot_id}~US", timeout=60000)
        await page.wait_for_selector("ul.data-list--details", timeout=10000)

        def get_text(label: str) -> str:
            return page.locator(f"li:has(span.data-list__label >> text={label}) span.data-list__value").first.text_content()

        info = {
            "Марка/Модель": await get_text("Vehicle:") or "—",
            "Гілка": await get_text("Selling Branch:") or "—",
            "Пошкодження": await get_text("Primary Damage:") or "—",
            "Title": await get_text("Title/Sale Doc:") or "—",
            "Статус VIN": await get_text("VIN (Status):") or "—",
            "Пробіг": await get_text("Odometer:") or "—",
            "Ключі": await get_text("Key:") or "—",
            "Подушки": await get_text("Airbags:") or "—",
            "Тип кузова": await get_text("Body Style:") or "—",
            "Двигун": await get_text("Engine:") or "—",
            "Аукціон": await get_text("Auction Date and Time:") or "—",
        }

        await browser.close()

        return f"""<b>🚗 IAAI Лот {lot_id}</b>
Марка/Модель: {info["Марка/Модель"]}
📍 Гілка: {info["Гілка"]}
🛠 Пошкодження: {info["Пошкодження"]}
📄 Title: {info["Title"]}
🧾 Статус VIN: {info["Статус VIN"]}
📉 Пробіг: {info["Пробіг"]}
🗝 Ключі: {info["Ключі"]}
🎈 Подушки: {info["Подушки"]}
🚘 Кузов: {info["Тип кузова"]}
🔧 Двигун: {info["Двигун"]}
⏰ Аукціон: {info["Аукціон"]}"""

# Для запуску:
# asyncio.run(get_iaai_full_info("42646912"))
