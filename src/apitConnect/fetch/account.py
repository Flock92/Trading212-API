async def fetch_account(self, x_trader_client: str):
    """
    Executes a fetch request within the current browser context
    to maintain session headers and cookies.
    """
    if not self.connector.page:
        raise RuntimeError("Browser page not initialized. Call connect() first.")

    url = f"https://{self.mode}.services.trading212.com/rest/v1/accounts"
    base_url = "https://app.trading212.com/"

    js_script = (
        "async () => {"
        f"  const response = await fetch('{url}', {{"
        "    headers: {"
        "      'accept': 'application/json',"
        "      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',"
        '      \'sec-ch-ua\': \'"Chromium";v="145", "Not:A-Brand";v="99"\','
        "      'sec-ch-ua-mobile': '?0',"
        "      'sec-ch-ua-platform': '\"Windows\"',"
        "      'sec-fetch-dest': 'empty',"
        "      'sec-fetch-mode': 'cors',"
        "      'sec-fetch-site': 'same-site',"
        f"      'x-trader-client': '{x_trader_client}',"
        "      'x-trader-device-model': 'Chrome'"
        "    },"
        f"   referrer: '{base_url}',"
        "    body: null,"
        "    method: 'GET',"
        "    mode: 'cors',"
        "    credentials: 'include'"
        "  },);"
        "  if (!response.ok) {"
        "    throw new Error('HTTP error! status: ' + response.status);"
        "  }"
        "  return await response.json();"
        "}"
    )

    try:
        return await self.connector.page.evaluate(js_script)
    except Exception as e:
        print(f"Fetch failed: {e}")
        return None
