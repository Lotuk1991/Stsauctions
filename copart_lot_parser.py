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
            title = await page.locator("label[data-uname='lotdetailTitledescription']").locator("..").locator("span span").text_content()
        except:
            title = "No title"

        try:
            location = await page.locator("label[data-uname='lotdetailSaleinformationlocationlabel']").locator("..").locator("span").text_content()
        except:
            location = "No location"

        try:
            engine = await page.locator("label[data-uname='lotdetailEngine']").locator("..").locator("span").text_content()
        except:
            engine = "No engine"

        try:
            fuel = await page.locator("label[data-uname='lotdetailFuel']").locator("..").locator("span").text_content()
        except:
            fuel = "No fuel"

        try:
            doc_type = await page.locator("label[data-uname='lotdetailTitledescription']").locator("..").locator("span span").text_content()
        except:
            doc_type = "No doc"

        try:
            vin = await page.locator("label[data-uname='lotdetailVin']").locator("..").locator("span").text_content()
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
