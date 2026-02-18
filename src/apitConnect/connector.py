from playwright.async_api import Page, TimeoutError, async_playwright
from playwright_stealth import stealth  # Use the standard stealth helper

from src.apitConnect.auth import StoredAuth


class Signal:
    def emit(self, *args, **kwargs):
        print(f"[Progress {args[0][0]}%]: {args[0][1]}")


class PlaywrightConnector:
    def __init__(self, base_url: str, headless: bool = True):
        self.base_url = base_url.rstrip("/")
        self.headless = headless
        self.progress = Signal()
        self.captured_headers = {}

        # Internal state to keep objects alive
        self.playwright = None
        self.browser = None
        self.page = None

    async def authenticate(
        self,
        username: str,
        password: str,
        login_path: str = "/login",
        remember_me: bool = True,
    ) -> StoredAuth:
        self.progress.emit((3, "Initializing Playwright"))

        # Start Playwright without 'with' to prevent auto-closure
        self.playwright = await async_playwright().start()

        self.progress.emit((6, "Launching Browser"))
        self.browser = await self.playwright.chromium.launch_persistent_context(
            user_data_dir="userdata",
            headless=self.headless,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--headless=new" if self.headless else "",
            ],
        )

        self.page = self.browser.pages[0]
        # Apply stealth manually since we aren't using the context manager
        await stealth.Stealth().apply_stealth_async(self.page)

        self.progress.emit((12, f"Loading login page {self.base_url}"))
        await self.page.goto(self.base_url + login_path, wait_until="load")
        await self.page.wait_for_timeout(2000)

        self.progress.emit((15, f"Filling username {username}"))
        try:
            email_input = self.page.locator('input[type="email"], input[name="email"]')
            await email_input.wait_for(state="visible", timeout=10000)
            await email_input.fill(username)
        except Exception as e:
            self.progress.emit((15, f"Email selector failed, trying fallback {e}"))
            await self.login_with_fallback(page=self.page, username=username)

        self.progress.emit((19, f"Filling password {'*' * len(password)}"))
        await self.page.locator('input[type="password"]').fill(password)

        if remember_me:
            try:
                await self.page.get_by_test_id("remember-me-checkbox").click(
                    timeout=2000
                )
            except Exception:
                pass

        self.page.on("request", self.capture_request_headers)

        self.progress.emit((28, "Submitting Login Form"))
        await self.page.get_by_test_id("login-form-log-in-button").click()

        self.progress.emit((32, "Waiting for authentication to process"))
        try:
            await self.page.wait_for_load_state("networkidle", timeout=15000)
        except TimeoutError:
            self.progress.emit((35, "Network didn't go idle, proceeding anyway"))

        self.progress.emit((37, "Extracting session data"))
        cookies = await self.browser.cookies()

        try:
            tokens = await self.page.evaluate("""() => ({
                access_token: window.localStorage.getItem('access_token'),
                refresh_token: window.localStorage.getItem('refresh_token'),
            })""")
        except Exception:
            tokens = {"access_token": None, "refresh_token": None}

        self.progress.emit((78, "Login completed - Browser remains open"))

        return StoredAuth(
            access_token=tokens.get("access_token"),
            refresh_token=tokens.get("refresh_token"),
            cookies=cookies,
            headers=self.captured_headers,
        )

    async def capture_request_headers(self, request):
        # We look for the main app config or trading requests which carry the 'x-trader' headers
        if "trading212.com" in request.url and "x-trader-client" in request.headers:
            self.captured_headers = request.headers
            # Optional: print(f"Captured Version: {request.headers['x-trader-client']}")

    async def shutdown(self):
        """Manual cleanup method with safety checks to prevent driver connection errors."""
        try:
            self.progress.emit((90, "Starting safe shutdown"))

            # 1. Close the page first
            if self.page:
                await self.page.close()

            # 2. Close the browser context (launch_persistent_context returns a context)
            if self.browser:
                # Check if the connection is still open before trying to close
                await self.browser.close()

            # 3. Finally, stop the Playwright driver process
            if self.playwright:
                await self.playwright.stop()

            self.progress.emit((100, "Playwright shut down safely"))

        except Exception as e:
            # Catch the "Connection closed" error specifically to keep the logs clean
            if "Connection closed" in str(e):
                self.progress.emit((100, "Shutdown: Connection closed (expected)"))
            else:
                print(f"Error during shutdown: {e}")

    async def login_with_fallback(self, page: Page, username):
        selectors = ["input[name='email']", "input[id='email']", "input[type='email']"]
        for sel in selectors:
            try:
                loc = page.locator(sel)
                if await loc.is_visible():
                    await loc.fill(username)
                    return
            except Exception:
                continue
        raise RuntimeError("Could not find email input.")
