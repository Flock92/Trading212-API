from playwright.async_api import TimeoutError
from src.apitConnect.core.auth.session import has_login_cookie
from src.apitConnect.event import Event, EventType, event_bus

eml_locators = 'input[type="email"], input[name="email"], input[autocomplete="email"]'
pwd_locators = 'input[type="password"], input[name="password"], input[autocomplete="password"]'

async def check_access_denied(page):
    """Checks for 'Access Denied' text and returns True if found."""
    # We use a broad selector to find the text anywhere on the page
    denied_text = page.get_by_text("ACCESS DENIED", exact=False)
    try:
        # Short timeout (2s) because we don't want to hang if the page is fine
        await denied_text.wait_for(state="attached", timeout=2000)
        return True
    except TimeoutError:
        return False

async def perform_login(base_url, page, username, password, retries=1):
    await page.goto(base_url + "/login", wait_until="load")

    # 1. Check for "Access Denied" immediately
    if await check_access_denied(page):
        if retries > 0:
            await event_bus.emit(Event.system("Access Denied detected. Refreshing page..."))
            await page.reload(wait_until="load")
            return await perform_login(base_url, page, username, password, retries - 1)
        else:
            raise Exception("Access Denied persists after refresh.")

    # 2. Check if already logged in
    if await has_login_cookie(page):
        return

    # 3. Attempt to find Email with a Refresh Catch
    try:
        email = page.locator(eml_locators)
        # We use a 5-10 second timeout for the first attempt
        await email.wait_for(state="visible", timeout=8000)
    except TimeoutError:
        if retries > 0:
            await event_bus.emit(Event.system("Email locator timeout. Retrying page load..."))
            await page.reload(wait_until="load")
            # Recurse once with retries decremented
            return await perform_login(base_url, page, username, password, retries - 1)
        else:
            raise Exception("Could not find email input after refreshing.")

    # 4. Normal fill and submit flow
    await email.fill(username)
    
    pwd = page.locator(pwd_locators)
    if await pwd.is_visible():
        await pwd.fill(password)

    await page.get_by_test_id("login-form-log-in-button").click()

    try:
        await page.wait_for_load_state("networkidle", timeout=15000)
    except TimeoutError:
        await event_bus.emit(Event.system("Post-login networkidle timeout (ignored)"))