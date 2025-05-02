import httpx
from bs4 import BeautifulSoup

async def get_iaai_full_info(lot_id: str) -> str:
    # 1. Отримуємо salvageId
    url_data = f"https://vis.iaai.com/Home/GetVehicleData?salvageId={lot_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url_data, headers=headers)
        if r.status_code != 200:
            return f"❌ IAAI помилка: {r.status_code}"
        base_data = r.json()
        salvage_id = base_data.get("SalvageId")
    except Exception as e:
        return f"❌ Не вдалося отримати salvageId: {e}"

    # 2. HTML-парсинг детальної сторінки
    url_html = f"https://www.iaai.com/VehicleDetail/{salvage_id}"
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url_html, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        def get_text(label):
            el = soup.find("div", class_="vehicle-info-label", string=label)
            if el and el.find_next_sibling("div"):
                return el.find_next_sibling("div").get_text(strip=True)
            return "—"

        return f"""
<b>🚗 IAAI Лот {lot_id}</b>
Марка/Модель: {get_text("VIN (Status):")}
📍 Гілка: {get_text("Selling Branch")}
🔧 Пошкодження: {get_text("Primary Damage")}
📜 Title: {get_text("Title/Sale Doc")}
🪪 Статус VIN: {get_text("VIN (Status):")}
"""
    except Exception as e:
        return f"❌ Не вдалося розпарсити HTML: {e}"
