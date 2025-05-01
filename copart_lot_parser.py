# copart_parser.py
from playwright.sync_api import sync_playwright
import json

def get_lot_info(lot_id: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        with open("cookies.json", "r") as f:
            context.add_cookies(json.load(f))

        page = context.new_page()
        page.goto("https://www.copart.com")

        url = f"https://www.copart.com/public/data/lotdetails/solr/{lot_id}"
        res = page.request.get(url)
        if res.status != 200:
            return f"❌ Лот {lot_id} не знайден."

        lot = res.json().get("data", {}).get("lotDetails", {})
        browser.close()

        return f"""📌 <b>Лот {lot_id}</b>
🚗 {lot.get('lcy')} {lot.get('lmg')} {lot.get('mkn')}
🔑 VIN: {lot.get('vin')}
📍 Локація: {lot.get('yn')} — {lot.get('ynm')}
📉 Пробіг: {lot.get('orr')} {lot.get('odometerBrand')}
💥 Пошкодження: {lot.get('sdd')} ({lot.get('cr')})
⛽ Двигун: {lot.get('ft')} ({lot.get('egn')})
🛒 Статус: {lot.get('lotSoldStatus')} ({lot.get('lotSold')})
"""
