from playwright.async_api import async_playwright
from playwright_stealth import stealth


async def apply_stealth(page):
    await stealth.Stealth().apply_stealth_async(page)

async def launch_browser(headless: bool):
    playwright = await async_playwright().start()

    browser = await playwright.chromium.launch_persistent_context(
        user_data_dir="userdata",
        headless=headless,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
        ],
    )

    page = browser.pages[0]

    await page.add_init_script("""
        const origFetch = window.fetch;
        window.fetch = (...args) => {
            console.log("FETCH:", args[0]);
            return origFetch(...args);
        };
    """)

    await apply_stealth(page=page)

    return playwright, browser, page