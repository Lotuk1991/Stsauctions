import httpx
from bs4 import BeautifulSoup

def get_iaai_full_info(lot_id: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # 1. Отримуємо справжній salvage_id
    try:
        r = httpx.get(f"https://vis.iaai.com/Home/GetVehicleData?salvageId={lot_id}", headers=headers)
        if r.status_code != 200:
            return f"❌ IAAI помилка: {r.status_code}"
        data = r.json()
        salvage_id = data.get("SalvageId")
        if not salvage_id:
            return "❌ Не вдалося отримати salvage_id"
    except Exception as e:
        return f"❌ Помилка запиту до IAAI: {e}"

    # 2. Парсимо сторінку деталі авто
    try:
        html_url = f"https://www.iaai.com/VehicleDetail/{salvage_id}~US"
        r = httpx.get(html_url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        def get_value(label):
            el = soup.find("div", string=label)
            if el and el.find_next_sibling("div"):
                return el.find_next_sibling("div").text.strip()
            return "—"

        info = {
            "Марка/Модель": get_value("Vehicle:"),
            "Гілка": get_value("Selling Branch:"),
            "Пошкодження": get_value("Primary Damage:"),
            "Title": get_value("Title/Sale Doc:"),
            "Статус VIN": get_value("VIN (Status):"),
            "Пробіг": get_value("Odometer:"),
            "Ключі": get_value("Key:"),
            "Подушки": get_value("Airbags:"),
            "Тип кузова": get_value("Body Style:"),
            "Двигун": get_value("Engine:"),
            "Дата аукціону": get_value("Auction Date and Time:"),
        }

        result = f"""<b>🚗 IAAI Лот {lot_id}</b>
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
⏰ Аукціон: {info["Дата аукціону"]}"""

        return result
    except Exception as e:
        return f"❌ Не вдалося спарсити сторінку IAAI: {e}"
