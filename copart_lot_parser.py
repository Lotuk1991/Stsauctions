import json
from playwright.async_api import async_playwright

async def get_lot_info(lot_number: str) -> dict:
    url = f"https://www.copart.com/lot/{lot_number}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Загрузка cookies
        try:
            with open("cookies.json", "r") as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
        except Exception as e:
            return {"error": f"Помилка з cookies: {e}", "url": url}

        page = await context.new_page()
        try:
            await page.goto(url, timeout=60000)
        except:
            await browser.close()
            return {"error": "Не вдалося завантажити сторінку", "url": url}

        content = await page.content()
        if "Page Not Found" in content or "captcha" in content.lower():
            await browser.close()
            return {"error": "Не вдалося завантажити сторінку", "url": url}

        # Извлечение информации
        def safe_get(selector):
            try:
                return page.locator(selector).first.inner_text()
            except:
                return "-"

        title = await safe_get("h1.title")
        location = await safe_get("label[data-uname='lotdetailSaleinformationlocationlabel'] + span")
        engine = await safe_get("span[data-uname='lotdetailEnginetype']")
        fuel = await safe_get("span[data-uname='lotdetailFuelvalue']")
        doc_type = await safe_get("span[data-uname='lotdetailTitledescriptionvalue'] span")
        vin = await safe_get("label[data-uname='lotdetailVin'] + div span")

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