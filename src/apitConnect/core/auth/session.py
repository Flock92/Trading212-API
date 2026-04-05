async def has_login_cookie(page):
    cookies = await page.context.cookies()
    return any(c["name"] == "LOGIN_TOKEN" for c in cookies)

def check_session(cookies, name: str) -> bool:
    return any(c["name"] == name for c in cookies)