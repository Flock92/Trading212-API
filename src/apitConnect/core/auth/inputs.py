async def fill_with_fallback(page, selectors, value):
    for sel in selectors:
        try:
            loc = page.locator(sel)
            if await loc.is_visible():
                await loc.fill(value)
                return True
        except:
            continue
    return False