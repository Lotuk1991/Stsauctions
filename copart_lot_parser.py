from playwright.async_api import async_playwright

async def get_lot_info(lot_number):
    url = f"https://www.copart.com/lot/{lot_number}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await (await browser.new_context()).new_page()

        await page.goto(url, timeout=60000)

        try:
            await page.wait_for_selector('h1', timeout=10000)
            title = await page.locator('h1').text_content() or "No title"
        except:
            title = "No title"

        try:
            location = await page.locator('.lot-details__location').text_content() or "No location"
        except:
            location = "No location"

        try:
            vin = await page.locator('[data-uname="lotdetailVINvalue"]').text_content() or "No VIN"
        except:
            vin = "No VIN"

        await browser.close()
        return {
            "title": title.strip(),
            "location": location.strip(),
            "vin": vin.strip(),
            "url": url
        }
