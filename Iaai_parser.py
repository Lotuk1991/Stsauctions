import json
from playwright.async_api import async_playwright

async def get_iaai_lot_info(lot_id: str, message) -> str:
    try:
        url = f"https://www.iaai.com/ru-ru/VehicleDetails/{lot_id}"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                locale="en-US",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                timezone_id="Europe/Kiev"
            )

            # Завантаження cookies
            try:
                with open("cookies_iaai.json", "r") as f:
                    await context.add_cookies(json.load(f))
            except Exception:
                return "❌ Не вдалося завантажити cookies"

            page = await context.new_page()
            await page.goto(url, timeout=60000)

            # Збереження HTML
            html = await page.content()
            with open("debug_iaai.html", "w", encoding="utf-8") as f:
                f.write(html)

            # Відправка файлу в Telegram
            await message.answer_document(open("debug_iaai.html", "rb"))

            # Очікування завантаження
            try:
                await page.wait_for_selector(".title-year", timeout=10000)
            except:
                return "❌ Сторінка IAAI не завантажилась"

            def get(selector):
                return page.locator(selector).nth(0).inner_text()

            year = await get(".title-year")
            make = await get(".title-make")
            model = await get(".title-model")
            vin = await get("span[data-uname='lotsearchLotdetailVIN']")
            location = await get("div[data-uname='lotdetailSaleInfo']")
            odometer = await get("li[data-uname='lotdetailOdometer']")
            damage = await get("li[data-uname='lotdetailDamage']")
            engine = await get("li[data-uname='lotdetailEngine']")
            image = await page.locator("img.main-image").nth(0).get_attribute("src")

            return f"""🔧 <b>IAAI Лот {lot_id}</b>
🚗 {year} {make} {model}
🆔 VIN: {vin}
📍 Локація: {location}
🧭 Пробіг: {odometer}
💥 Пошкодження: {damage}
⚙️ Двигун: {engine}
🖼 Фото: {image}
"""

    except Exception as e:
        return f"❌ Помилка IAAI: {e}"