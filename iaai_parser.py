import requests
from bs4 import BeautifulSoup
import re

def extract_lot_id_from_url(url: str) -> str:
    match = re.search(r'/VehicleDetail/(\d+)', url)
    return match.group(1) if match else None

def fetch_iaai_info(lot_url: str) -> dict:
    lot_id = extract_lot_id_from_url(lot_url)
    if not lot_id:
        return {"error": "❌ Не удалось извлечь ID из ссылки"}

    fs_url = "http://localhost:8191/v1"
    target_url = f"https://www.iaai.com/VehicleDetail/{lot_id}~US"

    payload = {
        "cmd": "request.get",
        "url": target_url,
        "maxTimeout": 60000
    }

    response = requests.post(fs_url, json=payload)
    result = response.json()

    if "solution" in result and "response" in result["solution"]:
        html_content = result["solution"]["response"]
        return parse_iaai_html(html_content)
    else:
        return {"error": "❌ Не удалось получить HTML-контент от FlareSolverr"}

def parse_iaai_html(html_content: str) -> dict:
    soup = BeautifulSoup(html_content, 'html.parser')

    def get_value(label):
        item = soup.find("span", string=lambda s: s and label in s)
        if item:
            parent = item.find_parent("li", class_="data-list__item")
            value = parent.find("span", class_="data-list__value") if parent else None
            return value.text.strip() if value else "—"
        return "—"

    return {
        "VIN": get_value("VIN"),
        "Odometer": get_value("Odometer"),
        "Location": get_value("Selling Branch"),
        "Loss": get_value("Loss"),
        "Primary Damage": get_value("Primary Damage"),
        "Title": get_value("Title/Sale Doc"),
        "Airbags": get_value("Airbags"),
        "Engine": get_value("Engine"),
        "Drive Line Type": get_value("Drive Line Type"),
        "Transmission": get_value("Transmission"),
        "Fuel Type": get_value("Fuel Type"),
        "Cylinders": get_value("Cylinders"),
        "Keys": get_value("Key"),
        "Auction Date": get_value("Auction Date and Time"),
    }

# Пример использования
if __name__ == "__main__":
    url = input("Вставьте ссылку на лот IAAI: ").strip()
    data = fetch_iaai_info(url)
    for key, value in data.items():
        print(f"{key}: {value}")
