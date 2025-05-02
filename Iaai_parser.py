import httpx
import json

def get_iaai_lot_info(lot_id):
    url = f"https://www.iaai.com/api/vehicle-lite/{lot_id}"

    with open("cookies_iaai.json", "r") as f:
        cookies = {c["name"]: c["value"] for c in json.load(f)}

    headers = {
        "user-agent": "Mozilla/5.0",
        "accept": "application/json",
        "referer": f"https://www.iaai.com/VehicleDetail/{lot_id}~US",
    }

    r = httpx.get(url, headers=headers, cookies=cookies)
    print("🔽 STATUS:", r.status_code)
    print("🔽 RESPONSE:", r.text[:500])  # первые 500 символов

    if r.status_code != 200:
        return f"❌ IAAI статус: {r.status_code}"

    if not r.text.strip():
        return "❌ IAAI: Пустой ответ. Возможно, блокировка или нужна авторизация."

    try:
        data = r.json()
        return f"✅ {data.get('Year')} {data.get('Make')} {data.get('Model')} VIN: {data.get('Vin')}"
    except Exception as e:
        return f"❌ IAAI ошибка: {e}"


