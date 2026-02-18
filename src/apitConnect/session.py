import asyncio
from typing import Any, Dict, List, Optional

import aiohttp
from yarl import URL


class AsyncSessionManager:
    """
    Manages an aiohttp ClientSession with automatic token refresh.
    Also supports full cookie synchronization from Playwright.
    """

    def __init__(
        self,
        base_url: str,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        refresh_endpoint: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._refresh_endpoint = refresh_endpoint
        self._session = session or aiohttp.ClientSession()
        self._lock = asyncio.Lock()

    async def close(self):
        await self._session.close()

    async def _refresh(self) -> bool:
        if not self._refresh_token or not self._refresh_endpoint:
            return False

        async with self._lock:
            url = URL(self.base_url) / self._refresh_endpoint.lstrip("/")
            payload = {"refresh_token": self._refresh_token}

            async with self._session.post(str(url), json=payload) as resp:
                if resp.status == 200:
                    body = await resp.json()
                    self._access_token = body.get("access_token")
                    if "refresh_token" in body:
                        self._refresh_token = body.get("refresh_token")
                    return True
                return False

    async def request(
        self, method: str, endpoint: str, retry: bool = True, **kwargs
    ) -> aiohttp.ClientResponse:
        url = str(URL(self.base_url) / endpoint.lstrip("/"))
        headers = kwargs.pop("headers", {}) or {}
        if self._access_token:
            headers.setdefault("Authorization", f"Bearer {self._access_token}")

        async with self._session.request(
            method, url, headers=headers, **kwargs
        ) as resp:
            if resp.status == 401 and retry:
                refreshed = await self._refresh()
                if refreshed:
                    return await self.request(method, endpoint, retry=False, **kwargs)
            return resp

    async def get(self, endpoint: str, **kwargs) -> aiohttp.ClientResponse:
        return await self.request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> aiohttp.ClientResponse:
        return await self.request("POST", endpoint, **kwargs)

    @property
    def access_token(self) -> Optional[str]:
        return self._access_token

    @property
    def refresh_token(self) -> Optional[str]:
        return self._refresh_token

    # Full cookie sync implementation
    def sync_playwright_cookies(self, playwright_cookies: List[Dict[str, Any]]):
        """
        Sync cookies from Playwright context into aiohttp cookie jar.
        Playwright cookie item example:
        {'name','value','domain','path','expires','httpOnly','secure','sameSite'}
        """
        jar = self._session.cookie_jar
        for c in playwright_cookies:
            name = c.get("name")
            value = c.get("value")
            domain = c.get("domain")
            path = c.get("path", "/")
            # Build a response_url that aiohttp's jar will accept
            # aiohttp expects a full URL; use scheme+domain+path
            scheme = "https" if c.get("secure") else "http"
            response_url = f"{scheme}://{domain}{path}"

            # prepare cookie attributes; aiohttp accepts update_cookies with a dict
            cookie_dict = {f"{name}": f"{value}"}
            jar.update_cookies(cookie_dict, response_url=URL(response_url))

        print(playwright_cookies)
