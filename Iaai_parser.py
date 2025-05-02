import httpx
import json
from bs4 import BeautifulSoup
from aiogram import types

def get_iaai_lot_info(lot_id: str, message: types.Message) -> str:
    url = f"https://www.iaai.com/api/vehicle-lite/{lot_id}"
    page_url = f"https://www.iaai.com/ru-ru/VehicleDetail/{lot_id}~US"

    try:
        with open("cookies_iaai.json", "r") as f:
            cookies = {c["name"]: c["value"] for c in json.load(f)}

        headers = {
            "user-agent": "Mozilla/5.0",
            "accept": "application/json",
            "referer": page_url
        }

        r = httpx.get(url, headers=headers, cookies=cookies, timeout=10)

        with open("debug_iaai.txt", "w", encoding="utf-8") as debug:
            debug.write(f"STATUS: {r.status_code}\n")
            debug.write(f"TEXT:\n{r.text[:1000]}")

        if r.status_code == 200 and r.text.strip():
            try:
                data = r.json()
                return f"""📌 <b>IAAI Лот {lot_id}</b>
🚗 {data.get('Year')} {data.get('Make')} {data.get('Model')}
🔑 VIN: {data.get('Vin')}
📍 Локація: {data.get('AuctionLocationName')}
📉 Пробіг: {data.get('Odometer')} {data.get('OdometerType')}
💥 Пошкодження: {data.get('LossType')} / {data.get('Damage')}
⛽ Двигун: {data.get('Engine')}
🖼 Фото: {data.get('ImageUrl')}
"""
            except Exception:
                pass

        return await parse_iaai_html_fallback(lot_id, cookies, message)

    except Exception as e:
        return f"❌ IAAI помилка: {e}"


async def parse_iaai_html_fallback(lot_id: str, cookies: dict, message: types.Message) -> str:
    url = f"https://www.iaai.com/ru-ru/VehicleDetail/{lot_id}~US"
    headers = {
        "user-agent": "Mozilla/5.0"
    }

    try:
        r = httpx.get(url, headers=headers, cookies=cookies)
        if r.status_code != 200:
            return f"❌ HTML статус: {r.status_code}"

        html_path = "debug_iaai.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(r.text)

        # отправляем HTML файл в Telegram
        with open(html_path, "rb") as f:
            await message.answer_document(types.InputFile(f), caption="📄 debug_iaai.html")

        soup = BeautifulSoup(r.text, "html.parser")

        def get_text(selector):
            el = soup.select_one(selector)
            return el.text.strip() if el else "—"

        vin = get_text("span[data-uname='lotdetailVIN']")
        year = get_text(".title-year")
        make = get_text(".title-make")
        model = get_text(".title-model")
        location = get_text("div[data-uname='lotdetailSaleInfo']")
        odometer = get_text("li[data-uname='lotdetailOdometer']")
        damage = get_text("li[data-uname='lotdetailPrimaryDamage']")
        engine = get_text("li[data-uname='lotdetailEngine']")
        img = soup.select_one("img.main-image")
        image_url = img["src"] if img else "—"

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
        return f"❌ Парсинг HTML помилка: {e}"
