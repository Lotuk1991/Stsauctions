import httpx
import json

def get_lot_info(lot_id: str) -> str:
    url = f"https://www.copart.com/public/data/lotdetails/solr/{lot_id}"

    try:
        with open("cookies.json", "r") as f:
            cookies = {c["name"]: c["value"] for c in json.load(f)}

        headers = {
            "user-agent": "Mozilla/5.0",
            "accept": "application/json",
            "referer": f"https://www.copart.com/lot/{lot_id}",
        }

        r = httpx.get(url, headers=headers, cookies=cookies, timeout=10)

        if r.status_code != 200:
            return f"❌ Copart статус: {r.status_code}"

        if not r.text.strip():
            return "❌ Copart повернув порожню відповідь. Можливо, cookies неактуальні або IP заблоковано."

        try:
            data = r.json()
        except Exception:
            return "❌ Помилка: Copart повернув не-JSON. Можливо, HTML або блокування."

        lot = data.get("data", {}).get("lotDetails", {})
        if not lot:
            return f"❌ Лот {lot_id} не знайдено або недоступний."

        return f"""📌 <b>Copart Лот {lot_id}</b>
🚗 {lot.get('lcy')} {lot.get('lmg')} {lot.get('mkn')}
🔑 VIN: {lot.get('fv')}
📍 Локація: {lot.get('yn')} — {lot.get('ynm')}
📉 Пробіг: {lot.get('orr')} {lot.get('odometerBrand')}
💥 Пошкодження: {lot.get('sdd')} ({lot.get('cr')})
⛽ Двигун: {lot.get('ft')} ({lot.get('egn')})
🛒 Статус: {lot.get('lotSoldStatus')} ({lot.get('lotSold')})
🖼 Фото: {lot.get('image')}/{lot.get('imageName')}
"""
    except Exception as e:
        return f"❌ Copart помилка: {e}"
