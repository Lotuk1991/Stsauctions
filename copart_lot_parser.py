def get_lot_info(lot_id: str) -> str:
    API_URL = f"https://www.copart.com/public/data/lotdetails/solr/{lot_id}"

    with open("cookies.json", "r") as f:
        cookies = {cookie["name"]: cookie["value"] for cookie in json.load(f)}

    headers = {
        "user-agent": "Mozilla/5.0",
        "accept": "application/json",
    }

    try:
        r = httpx.get(API_URL, headers=headers, cookies=cookies, timeout=10)

        if r.status_code != 200:
            return f"❌ Лот {lot_id} не знайден (код {r.status_code})"

        # защита от пустого ответа
        if not r.text or r.text.strip() == "":
            return f"❌ Відповідь пуста. Можливо, cookies недійсні."

        data = r.json()
        lot = data.get("data", {}).get("lotDetails", {})

        if not lot:
            return f"❌ Лот {lot_id} не знайден або неактивний."

        return f"""📌 <b>Лот {lot_id}</b>
🚗 {lot.get('lcy')} {lot.get('lmg')} {lot.get('mkn')}
🔑 VIN: {lot.get('vin')}
📍 Локація: {lot.get('yn')} — {lot.get('ynm')}
📉 Пробіг: {lot.get('orr')} {lot.get('odometerBrand')}
💥 Пошкодження: {lot.get('sdd')} ({lot.get('cr')})
⛽ Двигун: {lot.get('ft')} ({lot.get('egn')})
🛒 Статус: {lot.get('lotSoldStatus')} ({lot.get('lotSold')})
"""
    except Exception as e:
        return f"❌ Помилка: {e}"
