import json
from playwright.async_api import async_playwright

async def get_lot_info(lot_number: str) -> dict:
    url = f"https://www.copart.com/lot/{lot_number}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            context = await browser.new_context(storage_state="storage_state.json")
        except Exception as e:
            await browser.close()
            return {"error": f"❌ Помилка при завантаженні storage_state.json: {e}", "url": url}

        page = await context.new_page()
        try:
            await page.goto(url, timeout=60000)
        except:
            await browser.close()
            return {"error": "⚠️ Не вдалося завантажити сторінку", "url": url}

        content = await page.content()
        if "Page Not Found" in content or "captcha" in content.lower():
            await browser.close()
            return {"error": "⚠️ Не вдалося завантажити сторінку", "url": url}

        # Извлечение информации
        def safe(selector):
            try:
                return page.locator(selector).first.inner_text()
            except:
                return "-"

        try:
            title = await page.inner_text("h1.title")
        except:
            title = "-"

        location = await safe("label[data-uname='lotdetailSaleinformationlocationlabel'] + span")
        engine = await safe("span[data-uname='lotdetailEnginetype']")
        fuel = await safe("span[data-uname='lotdetailFuelvalue']")
        doc_type = await safe("span[data-uname='lotdetailTitledescriptionvalue'] span span")

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
            "url": url,
        }