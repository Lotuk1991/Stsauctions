import json
import httpx

async def get_iaai_lot_info(lot_id: str) -> str:
    url = f"https://vis.iaai.com/Home/GetVehicleData?salvageId={lot_id}"

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6",
        "referer": f"https://vis.iaai.com/Home/ThreeSixtyView?keys=SID-{lot_id}~STP-1~INT-1&iframeview=true",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    try:
        with open("cookies_iaai.json", "r") as f:
            cookies_raw = json.load(f)
            cookies = {c["name"]: c["value"] for c in cookies_raw}
    except Exception:
        return "❌ Не удалось загрузить cookies для IAAI"

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers, cookies=cookies)
        if r.status_code != 200:
            return f"❌ IAAI статус: {r.status_code}"

        data = r.json()
    except Exception as e:
        return f"❌ IAAI ошибка: {e}"

    try:
        vehicle = data

return f"""📌 <b>IAAI Лот {lot_id}</b>
🆔 Stock #: {vehicle.get('StockNumber')}
🔑 VIN: {vehicle.get('Vin')}
🏢 Branch #: {vehicle.get('AdministrativeBranchNumber')}
🛠 Тип: {vehicle.get('SalvageType')}"""

    except Exception:
        return "❌ Не удалось разобрать данные от IAAI"
