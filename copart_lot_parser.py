import httpx
import json

def get_lot_info(lot_id: str) -> str:
    url = f"https://www.copart.com/public/data/lotdetails/solr/{lot_id}"

    # Загружаем cookies
    with open("cookies.json", "r") as f:
        cookies = {c["name"]: c["value"] for c in json.load(f)}

    headers = {
        "user-agent": "Mozilla/5.0",
        "accept": "application/json",
        "referer": f"https://www.copart.com/lot/{lot_id}",
        "accept-language": "en-US,en;q=0.9",
    }

    try:
        r = httpx.get(url, headers=headers, cookies=cookies, timeout=10)

        # Логируем ответ в консоль
        print(f"📥 Status: {r.status_code}")
        print(f"📥 Body (first 500 chars):\n{r.text[:500]}")

        # Проверка на статус
        if r.status_code != 200:
            return f"❌ Статус {r.status_code}: Copart відмовився відповідати."

        # Проверка на пустой ответ
        if not r.text.strip():
            return "❌ Copart повернув порожню відповідь. Можливо, cookies недійсні або IP заблоковано."

        # Пробуем распарсить JSON
        try:
            data = r.json()
        except Exception:
            return "❌ Помилка: Copart повернув не-JSON. Можливо, тебе заблокували."

        # Проверка на отсутствие лота
        lot = data.get("data", {}).get("lotDetails", {})
        if not lot:
            return f"❌ Лот {lot_id} не знайдено або порожній."

        # Готовим сообщение
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
        return f"❌ Несподівана помилка: {e}"
