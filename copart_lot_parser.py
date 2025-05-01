# copart_lot_parser.py

from playwright.sync_api import sync_playwright
import json

def get_copart_lot_info(lot_id: str) -> str:
    COOKIES_FILE = "cookies.json"
    API_URL = f"https://www.copart.com/public/data/lotdetails/solr/{lot_id}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        with open(COOKIES_FILE, "r") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)

        page = context.new_page()
        page.goto("https://www.copart.com")

        response = page.request.get(API_URL)
        if response.status != 200:
            return f"❌ Лот {lot_id} не знайден (код {response.status})"

        data = response.json()
        lot = data.get("data", {}).get("lotDetails", {})

        result = f"""📌 <b>Інформація про лот {lot_id}</b>:
🚗 <b>Авто:</b> {lot.get('lcy')} {lot.get('lmg')} {lot.get('mkn')}
🔑 <b>VIN:</b> {lot.get('vin')}
📉 <b>Пробіг:</b> {lot.get('orr')} {lot.get('odometerBrand')}
📍 <b>Локація:</b> {lot.get('yn')} — {lot.get('ynm')}
⛽ <b>Двигун:</b> {lot.get('ft')} ({lot.get('egn')})
💥 <b>Пошкодження:</b> {lot.get('sdd')} ({lot.get('cr')})
🛒 <b>Статус:</b> {lot.get('lotSoldStatus')} ({lot.get('lotSold')})
"""
        browser.close()
        return result
