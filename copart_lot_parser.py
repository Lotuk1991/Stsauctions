from playwright.async_api import async_playwright

async def get_lot_info(lot_number):
    url = f"https://www.copart.com/lot/{lot_number}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url, timeout=60000)
        await page.wait_for_selector("h1", timeout=10000)

        # Название авто
        try:
            title = await page.locator("h1").text_content()
        except:
            title = "No title"

        # VIN
        try:
            vin_label = await page.query_selector('label[data-uname="lotdetailVin"]')
            vin_container = await vin_label.evaluate_handle("el => el.parentElement")
            vin_value = await vin_container.query_selector('.lot-details-desc')
            vin = await vin_value.inner_text()
        except:
            vin = "No VIN"

        # Title (Документ)
        try:
            title_label = await page.query_selector('label[data-uname="lotdetailTitledescription"]')
            title_container = await title_label.evaluate_handle("el => el.parentElement")
            title_span = await title_container.query_selector('.lot-details-desc span')
            doc_type = await title_span.inner_text()
        except:
            doc_type = "No Title Code"

        # Engine
        try:
            engine_label = await page.query_selector('label[data-uname="lotdetailEngine"]')
            engine_container = await engine_label.evaluate_handle("el => el.parentElement")
            engine_value = await engine_container.query_selector('.lot-details-desc')
            engine = await engine_value.inner_text()
        except:
            engine = "No engine"

        # Fuel
        try:
            fuel_label = await page.query_selector('label[data-uname="lotdetailFuel"]')
            fuel_container = await fuel_label.evaluate_handle("el => el.parentElement")
            fuel_value = await fuel_container.query_selector('.lot-details-desc')
            fuel = await fuel_value.inner_text()
        except:
            fuel = "No fuel"

        # Location
        try:
            loc_label = await page.query_selector('label[data-uname="lotdetailSaleinformationlocationlabel"]')
            loc_container = await loc_label.evaluate_handle("el => el.parentElement")
            loc_value = await loc_container.query_selector('span.lot-details-desc a')
            location = await loc_value.inner_text()
        except:
            location = "No location"

        await browser.close()

        return {
            "title": title.strip(),
            "vin": vin.strip(),
            "doc_type": doc_type.strip(),
            "engine": engine.strip(),
            "fuel": fuel.strip(),
            "location": location.strip(),
            "url": url
        }
