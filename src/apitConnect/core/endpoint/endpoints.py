from src.apitConnect.models.model import FetchScript
from typing import Union

referrer = "https://app.trading212.com"

# --- Account & Summary ---
ACCOUNT_ENDPOINT = FetchScript(
    name="accounts", endpoint="/rest/v1/accounts", method="GET", referrer=referrer
)

SUMMARY_ENDPOINT = FetchScript(
    name="summary",
    endpoint="/rest/v1/customers/accounts/summary",
    method="GET",
    description="Returns overall summary of account e.g. positions, funds",
    referrer=referrer,
)

# --- Market Data ---
SUPPORTED_TICKERS_ENDPOINT = FetchScript(
    name="supported tickers",
    endpoint="/rest/instrument-analyses/v1/summaries/supported-tickers",
    method="GET",
    description="Returns supported ticker symbols",
    referrer=referrer,
)

ADDITIONAL_INFO = FetchScript(
    name="additional info",
    endpoint="/rest/v2/value/trading-additional-info",
    method="GET",
    description="Get information on positions",
    referrer=referrer,
    # require_query_string logic can be handled by setting required_query_keys
)

# --- Trading & Orders ---
MARKET_VALUE_ORDER_ENDPOINT = FetchScript(
    name="market value order",
    endpoint="/rest/v2/cfd-trading/orders/market/value",
    method="POST",
    description="Execute market value order",
    require_body_dict=True,
    required_body_keys=["ticker", "value", "targetPrice"],
    optional_body_keys=[
        "stopLoss",
        "takeProfit",
    ],  # Example of adding visibility to options
    referrer=referrer,
)

# Pre-initialize the body for the user
MARKET_VALUE_ORDER_ENDPOINT.body = MARKET_VALUE_ORDER_ENDPOINT.get_template_body()

CLOSE_ORDER_ENDPOINT = FetchScript(
    name="close position",
    endpoint="/rest/v2/trading/open-positions/close",
    method="DELETE",
    description="Close open position",
    referrer=referrer,
)

SETTINGS_ENDPOINT = FetchScript(
    name="settings",
    endpoint="/rest/v3/cfd-trading/account/instruments/settings",
    method="POST",
    description="Returns instrument settings e.g. spread, ordersize",
    require_body_dict=True,
    required_body_keys=["ticker"],
    referrer=referrer,
)

# Pre-initialize the body for the user
SETTINGS_ENDPOINT.body = SETTINGS_ENDPOINT.get_template_body()

SWITCH_DEMO_LIVE_ENDPOINT = FetchScript(
    name="switch",
    endpoint="/rest/v4/login/session?skipVersionCheck=false",
    method="POST",
    description="Switch between a live and demo account",
    require_body_dict=True,
    required_body_keys=["accountId"],
    referrer=referrer,
)


Api_endpoint = Union[
    ACCOUNT_ENDPOINT, 
    SUMMARY_ENDPOINT, 
    SUMMARY_ENDPOINT, 
    ADDITIONAL_INFO, 
    MARKET_VALUE_ORDER_ENDPOINT, 
    MARKET_VALUE_ORDER_ENDPOINT, 
    CLOSE_ORDER_ENDPOINT,
    SETTINGS_ENDPOINT,
    SWITCH_DEMO_LIVE_ENDPOINT
    ]