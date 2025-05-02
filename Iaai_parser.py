import json
from playwright.sync_api import sync_playwright

def get_iaai_lot_via_playwright(lot_id: str) -> str:
    try:
        url = f"https://www.iaai.com/ru-ru/VehicleDetail/{lot_id}~US"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()

            with open("cookies_iaai.json", "r") as f:
                context.add_cookies(json.load(f))

            page = context.new_page()
            page.goto(url, timeout=60000)

            page.wait_for_selector(".title-year", timeout=15000)

            def get(selector):
                try:
                    return page.locator(selector).nth(0).inner_text().strip()
                except:
                    return "—"

            def get_attr(selector, attr):
                try:
                    return page.locator(selector).nth(0).get_attribute(attr)
                except:
                    return "—"

            year = get(".title-year")
            make = get(".title-make")
            model = get(".title-model")
            vin = get("span[data-uname='lotdetailVIN']")
            location = get("div[data-uname='lotdetailSaleInfo']")
            odometer = get("li[data-uname='lotdetailOdometer']")
            damage = get("li[data-uname='lotdetailPrimaryDamage']")
            engine = get("li[data-uname='lotdetailEngine']")
            image_url = get_attr("img.main-image", "src")

            browser.close()

            return f"""📌 <b>IAAI Лот {lot_id}</b>
🚗 {year} {make} {model}
🔑 VIN: {vin}
📍 Локація: {location}
📉 Пробіг: {odometer}
💥 Пошкодження: {damage}
⛽ Двигун: {engine}
🖼 Фото: {image_url}
"""
    except Exception as e:
        return f"❌ Помилка Playwright: {e}"
