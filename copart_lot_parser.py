import json
from playwright.async_api import async_playwright

async def get_lot_info(lot_number: str) -> dict:
    url = f"https://www.copart.com/lot/{lot_number}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Загружаем cookies
        with open("cookies.json", "r") as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto(url, timeout=60000)

        try:
            await page.wait_for_selector(".lot-details-desc", timeout=10000)
        except:
            return {"title": "Page not loaded", "location": "-", "engine": "-", "fuel": "-", "doc_type": "-", "vin": "-", "url": url}

        def safe(selector):
            try:
                return page.locator(selector).nth(0).inner_text()
            except:
                return "-"

        # Используем актуальные селекторы из твоего HTML:
        title = await safe("label[data-uname='lotdetailTitledescription'] + span span")
        location = await safe("label[data-uname='lotdetailSaleinformationlocationlabel'] + span a")
        engine = await safe("label[data-uname='lotdetailEngine'] + div span")
        fuel = await safe("label[data-uname='lotdetailFuel'] + span")
        doc_type = title  # Пока что, он дублируется из title
        vin = await safe("label[data-uname='lotdetailVin'] + div span")

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