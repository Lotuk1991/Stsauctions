import httpx
from bs4 import BeautifulSoup

async def get_iaai_full_info(lot_id: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # Замість прямого запиту — використовуємо проксі
        r = httpx.get(f"https://iaai.lotuk1991.workers.dev/?lot_id={lot_id}", headers=headers)
        if r.status_code != 200:
            return f"❌ Проксі помилка: {r.status_code}"
        soup = BeautifulSoup(r.text, "html.parser")

        def get_value(label: str) -> str:
            for item in soup.select(".data-list__item"):
                key = item.select_one(".data-list__label")
                val = item.select_one(".data-list__value")
                if key and val and label.lower() in key.text.strip().lower():
                    return val.text.strip()
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
            "Привід": get_value("Drive Line Type:"),
            "Паливо": get_value("Fuel Type:"),
            "Аукціон": get_value("Auction Date and Time:"),
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
🛞 Привід: {info["Привід"]}
⛽ Паливо: {info["Паливо"]}
⏰ Аукціон: {info["Аукціон"]}"""

        return result

    except Exception as e:
        return f"❌ Парсинг через проксі не вдався: {e}"
