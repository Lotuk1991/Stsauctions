import json
from playwright.async_api import async_playwright

async def get_iaai_lot_info(lot_id: str) -> str:
    try:
        url = f"https://www.iaai.com/ru-ru/VehicleDetail/{lot_id}~US"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()

            try:
                with open("cookies_iaai.json", "r") as f:
                    await context.add_cookies(json.load(f))
            except Exception:
                return "❌ Не вдалося завантажити cookies"

            page = await context.new_page()
            await page.goto(url, timeout=60000)

            try:
                await page.wait_for_selector(".title-year", timeout=15000)
            except:
                return "❌ Сторінка IAAI не завантажилась"

            def get(selector):
                return page.locator(selector).nth(0)

            year = await get(".title-year").inner_text()
            make = await get(".title-make").inner_text()
            model = await get(".title-model").inner_text()
            vin = await get("span[data-uname='lotdetailVIN']").inner_text()
            location = await get("div[data-uname='lotdetailSaleInfo']").inner_text()
            odometer = await get("li[data-uname='lotdetailOdometer']").inner_text()
            damage = await get("li[data-uname='lotdetailPrimaryDamage']").inner_text()
            engine = await get("li[data-uname='lotdetailEngine']").inner_text()
            image = await get("img.main-image").get_attribute("src")

            await browser.close()

            return f"""📌 <b>IAAI Лот {lot_id}</b>
🚗 {year} {make} {model}
🔑 VIN: {vin}
📍 Локація: {location}
📉 Пробіг: {odometer}
💥 Пошкодження: {damage}
⛽ Двигун: {engine}
🖼 Фото: {image}
"""
    except Exception as e:
        return f"❌ Playwright помилка: {e}"