import httpx
import json

def get_iaai_lot_info(lot_id):
    url = f"https://www.iaai.com/api/vehicle-lite/{lot_id}"

    with open("cookies_iaai.json", "r") as f:
        cookies = {cookie['name']: cookie['value'] for cookie in json.load(f)}

    headers = {
        "user-agent": "Mozilla/5.0",
        "accept": "application/json",
        "referer": f"https://www.iaai.com/ru-ru/VehicleDetail/{lot_id}",
    }

    r = httpx.get(url, headers=headers, cookies=cookies)
    print("🔍 Status:", r.status_code)
    print("📦 Body:", r.text[:300])  # покажи первые 300 символов

    if r.status_code != 200:
        return f"❌ IAAI статус: {r.status_code}"

    try:
        data = r.json()
        return f"✅ Лот: {data.get('Year')} {data.get('Make')} {data.get('Model')}"
    except Exception as e:
        return f"❌ IAAI ошибка: {e}"

