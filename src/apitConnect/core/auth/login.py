from playwright.async_api import TimeoutError
from src.apitConnect.core.auth.session import has_login_cookie
from src.apitConnect.event import event_bus


eml_locators = 'input[type="email"], input[name="email"], input[autocomplete="email"]'
pwd_locators = 'input[type="password"] , input[name="password"], input[autocomplete="password"]'


async def perform_login(base_url, page, username, password):
    await page.goto(base_url + "/login", wait_until="load")

    has_login = await has_login_cookie(page)

    if has_login:
        return

    # Fill email
    email = page.locator(eml_locators)
    await email.wait_for(state="visible")

    if await email.is_visible():
        await email.fill(username)

    # Fill password
    pwd = page.locator(pwd_locators)

    if await pwd.is_visible():
        await pwd.fill(password)

    await page.get_by_test_id("login-form-log-in-button").click()

    try:
        await page.wait_for_load_state("networkidle", timeout=15000)
    except TimeoutError:
        pass