import json
from playwright.async_api import async_playwright

async def get_lot_info(lot_number: str) -> dict:
    url = f"https://www.copart.com/lot/{lot_number}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Загрузка cookies
        with open("cookies.json", "r") as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto(url, timeout=60000)

        # Извлечение информации
        try:
            title = await page.inner_text("label[data-uname='lotdetailTitledescription'] + span span")  # Название
        except:
            title = "No title"

        try:
            location = await page.inner_text("label[data-uname='lotdetailSaleinformationlocationlabel'] + span")  # Локация
        except:
            location = "No location"

        try:
            engine = await page.inner_text("label[data-uname='lotdetailEngine'] + div span")  # Двигатель
        except:
            engine = "No engine"

        try:
            fuel = await page.inner_text("label[data-uname='lotdetailFuel'] + span")  # Топливо
        except:
            fuel = "No fuel"

        try:
            doc_type = await page.inner_text("label[data-uname='lotdetailTitledescription'] + span span")  # Документ
        except:
            doc_type = "No doc"

        try:
            vin = await page.inner_text("label[data-uname='lotdetailVin'] + div span")  # VIN
        except:
            vin = "No VIN"

        await browser.close()

        return {
            "title": title.strip(),
            "location": location.strip(),
            "engine": engine.strip(),
            "fuel": fuel.strip(),
            "doc_type": doc_type.strip(),
            "vin": vin.strip(),
            "url": url,
        }
