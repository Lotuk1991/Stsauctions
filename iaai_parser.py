import httpx
from bs4 import BeautifulSoup
import json

def get_iaai_full_info(lot_id: str) -> str:
    # 1. Получаем настоящий Salvage ID
    url_data = f"https://vis.iaai.com/Home/GetVehicleData?salvageId={lot_id}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = httpx.get(url_data, headers=headers)
        if r.status_code != 200:
            return f"❌ IAAI ошибка: {r.status_code}"
        base_data = r.json()
        salvage_id = base_data.get("SalvageId")
    except Exception as e:
        return f"❌ Не удалось получить данные о лоте: {e}"

    # 2. HTML-парсинг страницы VehicleDetail
    url_html = f"https://www.iaai.com/VehicleDetail/{salvage_id}"
    try:
        r = httpx.get(url_html, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        def get_text(label):
            block = soup.find("div", string=lambda t: t and label in t)
            if block and block.find_next("div"):
                return block.find_next("div").text.strip()
            return "—"

        vin = soup.select_one("div[data-uname='lotdetailVin']")
        vin_text = vin.text.strip() if vin else "—"

        branch = get_text("Selling Branch")
        damage = get_text("Primary Damage")
        loss = get_text("Loss")
        odometer = get_text("Odometer")
        title = get_text("Title/Sale Doc")
        model_tag = soup.select_one("h1")
        model = model_tag.text.strip() if model_tag else "—"

        image_tag = soup.select_one(".image-gallery img")
        image = image_tag["src"] if image_tag else "—"

        return f"""<b>🚘 IAAI Лот {lot_id}</b>
{model}
🔑 VIN: {vin_text}
📍 Локация: {branch}
📉 Пробег: {odometer}
💥 Повреждения: {loss} / {damage}
📄 Документ: {title}
🖼️ Фото: {image}"""
    except Exception as e:
        return f"❌ Не удалось спарсить HTML IAAI: {e}"
