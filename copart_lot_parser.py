import json
from playwright.async_api import async_playwright

async def get_lot_info(lot_number: str) -> dict:
    url = f"https://www.copart.com/lot/{lot_number}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        try:
            with open("cookies.json", "r") as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
        except Exception as e:
            return {"error": f"Ошибка загрузки cookies: {e}"}

        page = await context.new_page()
        try:
            await page.goto(url, timeout=60000)
            await page.wait_for_selector("label[data-uname='lotdetailVin']", timeout=15000)
        except Exception as e:
            await browser.close()
            return {"error": f"Ошибка загрузки страницы: {e}"}

        def safe_text(selector):
            try:
                return page.inner_text(selector)
            except:
                return None

        title = await safe_text("label[data-uname='lotdetailTitledescription'] + span span") or "No title"
        location = await safe_text("label[data-uname='lotdetailSaleinformationlocationlabel'] + span") or "No location"
        engine = await safe_text("label[data-uname='lotdetailEngine'] + div span") or "No engine"
        fuel = await safe_text("label[data-uname='lotdetailFuel'] + span") or "No fuel"
        doc_type = await safe_text("label[data-uname='lotdetailTitledescription'] + span span") or "No doc"
        vin = await safe_text("label[data-uname='lotdetailVin'] + div span") or "No VIN"

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