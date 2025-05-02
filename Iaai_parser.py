import httpx
import json

def get_iaai_lot_info(lot_id: str) -> str:
    url = f"https://www.iaai.com/api/vehicle-lite/{lot_id}"

    try:
        # Загружаем cookies
        with open("cookies_iaai.json", "r") as f:
            cookies = {c["name"]: c["value"] for c in json.load(f)}

        headers = {
            "user-agent": "Mozilla/5.0",
            "accept": "application/json",
            "referer": f"https://www.iaai.com/VehicleDetail/{lot_id}~US",
        }

        r = httpx.get(url, headers=headers, cookies=cookies, timeout=10)

        # 🔽 Отладка: лог в файл
        with open("debug_iaai.txt", "w", encoding="utf-8") as debug:
            debug.write(f"STATUS: {r.status_code}\n")
            debug.write(f"TEXT:\n{r.text[:1000]}")

        if r.status_code != 200:
            return f"❌ IAAI статус: {r.status_code}"

        if not r.text.strip():
            return "❌ IAAI: Порожня відповідь. Можливо, заблоковано або cookies не діють."

        try:
            data = r.json()
        except Exception:
            return "❌ IAAI повернув не JSON. Можливо, HTML або редирект."

        # ✅ Формируем красивый ответ
        return f"""📌 <b>IAAI Лот {lot_id}</b>
🚗 {data.get('Year')} {data.get('Make')} {data.get('Model')}
🔑 VIN: {data.get('Vin')}
📍 Локація: {data.get('AuctionLocationName')}
📉 Пробіг: {data.get('Odometer')} {data.get('OdometerType')}
💥 Пошкодження: {data.get('LossType')} / {data.get('Damage')}
⛽ Двигун: {data.get('Engine')}
🖼 Фото: {data.get('ImageUrl')}
"""
    except Exception as e:
        return f"❌ IAAI помилка: {e}"
