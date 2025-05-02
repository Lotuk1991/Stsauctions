import httpx
from bs4 import BeautifulSoup

def get_iaai_full_info(lot_id: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = httpx.get(f"https://vis.iaai.com/Home/GetVehicleData?salvageId={lot_id}", headers=headers)
        r.raise_for_status()
        data = r.json()
        salvage_id = data.get("SalvageId")
        if not salvage_id:
            return "❌ Не вдалося отримати salvage_id"
    except Exception as e:
        return f"❌ Помилка запиту до IAAI: {e}"

    try:
        html_url = f"https://www.iaai.com/VehicleDetail/{salvage_id}~US"
        r = httpx.get(html_url, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        def extract_value(label):
            for li in soup.select("ul.data-list--details > li.data-list__item"):
                label_span = li.select_one("span.data-list__label")
                value_span = li.select_one("span.data-list__value")
                if label_span and value_span and label.lower() in label_span.text.strip().lower():
                    return value_span.text.strip()
            return "—"

        info = {
            "Марка/Модель": extract_value("Vehicle:"),
            "Гілка": extract_value("Selling Branch:"),
            "Пошкодження": extract_value("Primary Damage:"),
            "Title": extract_value("Title/Sale Doc:"),
            "Статус VIN": extract_value("VIN (Status):"),
            "Пробіг": extract_value("Odometer:"),
            "Ключі": extract_value("Key:"),
            "Подушки": extract_value("Airbags:"),
            "Тип кузова": extract_value("Body Style:"),
            "Двигун": extract_value("Engine:"),
            "Аукціон": extract_value("Auction Date and Time:")
        }

        return f"""<b>🚗 IAAI Лот {lot_id}</b>
Марка/Модель: {info["Марка/Модель"]}
📍 Гілка: {info["Гілка"]}
🛠 Пошкодження: {info["Пошкодження"]}
📄 Title: {info["Title"]}
🧾 Статус VIN: {info["Статус VIN"]}
📉 Пробіг: {info["Пробіг"]}
🗝 Ключі: {info["Ключі"]}
🎈 Подушки: {info["Подушки"]}
🚘 Кузов: {info["Тип кузова"]}
🔧 Двигун: {info["Двигун"]}
⏰ Аукціон: {info["Аукціон"]}"""
    except Exception as e:
        return f"❌ Не вдалося спарсити HTML: {e}"
