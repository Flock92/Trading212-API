from src.apitConnect.models.model import _Client

async def graceful_shutdown(client: _Client):

    if client.page and not client.page.is_closed():
        await client.page.evaluate("""
            async () => {
                localStorage.clear();
                sessionStorage.clear();
                const dbs = await window.indexedDB.databases();
                dbs.forEach(db => window.indexedDB.deleteDatabase(db.name));
            }
        """)

    if client.browser:
        await client.browser.close()

    if client.playwright:
        await client.playwright.stop()