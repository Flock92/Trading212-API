import json


async def value(
    self,
    x_trader_client: str,
    ticker: str,
    value: float,
    target_price: float,
    stoploss: float = 0.0,
    takeprofit: float = 0.0,
):
    """
    Executes a fetch request within the current browser context
    to maintain session headers and cookies.
    """

    if not self.connector.page:
        raise RuntimeError("Browser page not initialized. Call connect() first.")

    url = f"https://{self.mode}.services.trading212.com/rest/v2/cfd-trading/orders/market/value"
    base_url = "https://app.trading212.com/"

    payload = {"ticker": {ticker}, "value": value, "targetPrice": target_price}

    if stoploss != 0.0:
        payload["stopLoss"] = stoploss

    if takeprofit != 0.0:
        payload["takeProfit"] = takeprofit

    json_payload = json.dumps(payload)

    js_script = (
        "async () => {"
        f"  const response = await fetch('{url}', {{"
        "    method: 'POST',"
        "    headers: {"
        "      'accept': 'application/json',"
        "      'content-type': 'application/json',"
        "      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',"
        '      \'sec-ch-ua\': \'"Chromium";v="145", "Not:A-Brand";v="99"\','
        "      'sec-ch-ua-mobile': '?0',"
        "      'sec-ch-ua-platform': '\"Windows\"',"
        "      'sec-fetch-dest': 'empty',"
        "      'sec-fetch-mode': 'cors',"
        "      'sec-fetch-site': 'same-site',"
        f"     'x-trader-client': '{x_trader_client}',"
        "      'x-trader-device-model': 'Chrome'"
        "    },"
        f"    referrer: '{base_url}',"
        f"    body: '{json_payload}',"  # Wrapped in quotes to be a string literal
        "    mode: 'cors',"
        "    credentials: 'include'"
        "  });"
        "  if (!response.ok) {"
        "    const errorText = await response.text();"  # Helps debug 400 errors
        "    throw new Error('Status ' + response.status + ': ' + errorText);"
        "  }"
        "  return await response.json();"
        "}"
    )

    try:
        return await self.connector.page.evaluate(js_script)
    except Exception as e:
        print(f"Fetch failed: {e}")
        return None
