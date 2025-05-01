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

        try:
            await page.wait_for_selector("h1.title", timeout=15000)
        except:
            return {"error": "Не вдалося завантажити сторінку", "url": url}

        # Извлечение всех данных
        def safe(selector):
            try:
                return page.locator(selector).nth(0).inner_text()
            except:
                return "-"

        try:
            title = await page.inner_text("h1.title")
        except:
            title = "-"

        try:
            location = await page.inner_text("a[data-uname='lotdetailSaleinformationlocationvalue']")
        except:
            location = "-"

        try:
            engine = await page.inner_text("span[data-uname='lotdetailEnginetype']")
        except:
            engine = "-"

        try:
            fuel = await page.inner_text("span[data-uname='lotdetailFuelvalue']")
        except:
            fuel = "-"

        try:
            doc_type = await page.inner_text("span[data-uname='lotdetailTitledescriptionvalue'] span span")
        except:
            doc_type = "-"

        try:
            vin = await page.locator("label[data-uname='lotdetailVin']").locator("..").locator("..").locator("span.lot-details-desc").inner_text()
        except:
            vin = "-"

        await browser.close()

        return {
            "title": title.strip(),
            "location": location.strip(),
            "engine": engine.strip(),
            "fuel": fuel.strip(),
            "doc_type": doc_type.strip(),
            "vin": vin.strip(),
            "url": url
        }