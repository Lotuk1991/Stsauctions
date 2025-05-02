import httpx
import json

def get_iaai_lot_info(lot_id: str) -> str:
    url = f"https://vis.iaai.com/Home/GetVehicleData?salvageId={lot_id}"

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6",
        "referer": f"https://vis.iaai.com/Home/ThreeSixtyView?keys=SID-{lot_id}~STP-1~INT-1&iframeview=true",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    try:
        with open("cookies_iaai.json", "r") as f:
            cookies = json.load(f)
        cookies_dict = {c["name"]: c["value"] for c in cookies}
    except Exception:
        return "❌ Не удалось загрузить cookies для IAAI"

    try:
        r = httpx.get(url, headers=headers, cookies=cookies_dict)
        if r.status_code != 200:
            return f"❌ IAAI статус: {r.status_code}"

        data = r.json()
    except Exception as e:
        return f"❌ IAAI ошибка: {e}"

    try:
        vehicle = data.get("Vehicles", [{}])[0]
        return f"""🔧 <b>IAAI Лот {lot_id}</b>
🚘 {vehicle.get('Year')} {vehicle.get('Make')} {vehicle.get('Model')}
🔑 VIN: {vehicle.get('Vin')}
📍 Локація: {vehicle.get('AuctionName')}
📏 Пробіг: {vehicle.get('Odometer')} {vehicle.get('OdometerType')}
💥 Пошкодження: {vehicle.get('LossType')} / {vehicle.get('Damage')}
🧠 Двигун: {vehicle.get('Engine')}
🖼 Фото: {vehicle.get('PrimaryImageUrl')}"""
    except Exception:
        return "❌ Не удалось разобрать данные от IAAI"
