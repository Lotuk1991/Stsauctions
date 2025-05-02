import httpx
import json

async def get_iaai_lot_info(lot_id: str) -> str:
    url = f"https://iaai.lotuk1991.workers.dev/VehicleDetail/{lot_id}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30)
            if response.status_code != 200:
                return f"❌ IAAI статус: {response.status_code}"
            data = response.json()
    except Exception as e:
        return f"❌ IAAI помилка: {e}"

    lot = data.get("data", {})

    if not lot:
        return f"❌ Лот {lot_id} не знайдено або порожній"

    return f"""🔧 <b>IAAI Лот {lot_id}</b>
🚗 {lot.get('Year')} {lot.get('Make')} {lot.get('Model')}
🔑 VIN: {lot.get('Vin')}
📍 Локація: {lot.get('AuctionLocationName')}
📏 Пробіг: {lot.get('Odometer')} {lot.get('OdometerType')}
💥 Пошкодження: {lot.get('LossType')} / {lot.get('Damage')}
🛠 Двигун: {lot.get('Engine')}
🖼 Фото: {lot.get('imageURL')}/{lot.get('imageName')}
"""
