import httpx
import json

def get_iaai_lot_info(lot_id: str) -> str:
    url = f"https://www.iaai.com/api/vehicle-lite/{lot_id}"

    # Загружаем cookies
    with open("cookies_iaai.json", "r") as f:
        cookies = {c["name"]: c["value"] for c in json.load(f)}

    headers = {
        "user-agent": "Mozilla/5.0",
        "accept": "application/json",
        "referer": f"https://www.iaai.com/VehicleDetail/{lot_id}~US",
    }

    try:
        r = httpx.get(url, headers=headers, cookies=cookies, timeout=10)

        print(f"📥 Status: {r.status_code}")
        print(f"📥 Body (first 500):\n{r.text[:500]}")

        if r.status_code != 200:
            return f"❌ IAAI статус: {r.status_code}"

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
    except Exception as e:
        return f"❌ IAAI помилка: {e}"es 
