import json
from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode
import playwright


@dataclass
class _Client:
    playwright: Any
    browser: Any
    page: Any
    headers: Dict[str, str]
    auth: _Auth


@dataclass
class _Auth:
    _x_trader: Any
    _account_id: Any
    _demo_session: Any
    _live_session: Any

    def __repr__(self):
        return (
            f"_Client(playwright={self.playwright}, browser={self.browser}, page={self.page}, "
            f"headers={self.headers}, _x_trader=***, _account_id=***, "
            f"_demo_session=***, _live_session=***)"
        )

class PositionSide(Enum):
    LONG = "LONG"
    SHORT = "SHORT"

class PositionStatus(Enum):
    PENDING = "PENDING"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    CLOSED = "CLOSED"

class ServiceURL(Enum):
    BASEURL = "https://app.trading212.com/"
    DEMO = "https:://demo.services.trading212.com"
    LIVE = "https:://live.services.trading212.com"


@dataclass
class FetchScript:
    endpoint: str
    base: str = ""
    query: Dict[str, Any] = field(default_factory=dict)
    name: str = ""
    description: str = ""
    method: str = "GET"
    x_trader_client: str = ""
    referrer: Optional[str] = None
    body: Optional[Union[dict, str]] = None
    mode: str = "cors"
    credentials: str = "include"
    return_json: bool = True
    require_body_dict: bool = False
    required_body_keys: List[str] = field(default_factory=list)
    optional_body_keys: List[str] = field(default_factory=list)

    # -------------------
    # Copy / template helpers
    # -------------------
    def copy_with(self, **changes) -> "FetchScript":
        """Return a new instance with updated values; template stays unchanged."""
        return replace(self, **changes)

    # -------------------
    # URL helpers
    # -------------------
    @property
    def url(self) -> str:
        """Dynamically builds the URL string."""
        if not self.base:
            full_url = self.endpoint
        else:
            full_url = f"{self.base.rstrip('/')}/{self.endpoint.lstrip('/')}"
        if self.query:
            connector = "&" if "?" in full_url else "?"
            full_url = f"{full_url}{connector}{urlencode(self.query)}"
        return full_url

    # -------------------
    # Body helpers
    # -------------------
    def get_template_body(self) -> Dict[str, None]:
        keys = self.required_body_keys + self.optional_body_keys
        return {k: None for k in keys}

    def validate(self):
        """Ensures body requirements are met."""
        if not self.require_body_dict and not self.required_body_keys:
            return

        if self.body is None:
            raise ValueError(f"[{self.name}] Body is required but currently None.")

        if self.require_body_dict and not isinstance(self.body, dict):
            raise TypeError(
                f"[{self.name}] body must be a dict, got {type(self.body).__name__}"
            )

        if self.required_body_keys and isinstance(self.body, dict):
            missing = [
                k
                for k in self.required_body_keys
                if k not in self.body or self.body[k] is None
            ]
            if missing:
                raise KeyError(
                    f"[{self.name}] Missing required body keys: {', '.join(missing)}"
                )

    def _format_body(self) -> str:
        if self.body is None or self.method.upper() in ["GET", "HEAD"]:
            return "null"
    
        if isinstance(self.body, dict):
            # 1. Filter out None values
            filtered_payload = {k: v for k, v in self.body.items() if v is not None}
        
            # 2. Key Change: Use separators to ensure "accountId":41133754 (no space)
            payload = json.dumps(filtered_payload, separators=(',', ':'))
        else:
            payload = self.body

        # 3. Return the raw string (the JS template will handle the fetch formatting)
        # If your JS template looks like: body: {body_from_python}, 
        # then payload should NOT have extra quotes here if it's already a JSON string.
        return payload

    def to_js(self) -> str:
        """Returns a complete JS fetch function string."""
        self.validate()
        body_str = self._format_body()
        ref_line = f"    referrer: '{self.referrer}'," if self.referrer else ""
        return (
            "async () => {"
            f"  const response = await fetch('{self.url}', {{"
            "    headers: {"
            "      'accept': 'application/json',"
            "      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',"
            '      \'sec-ch-ua\': \'"Chromium";v="145", "Not:A-Brand";v="99"\','
            "      'sec-fetch-dest': 'empty',"
            "      'sec-fetch-mode': 'cors',"
            "       'Connection': 'keep-alive',"
            "      'content-type': 'application/json',"
            "      'sec-fetch-site': 'same-site',"
            f"      'x-trader-client': '{self.x_trader_client}',"
            "      'x-trader-device-model': 'Chrome'"
            "    },"
            f"    {ref_line}"
            f"    body: {body_str},"
            f"    method: '{self.method}',"
            f"    mode: '{self.mode}',"
            f"    credentials: 'include'"
            "  },);"
            "  if (!response.ok) {"
            "    const errorText = await response.text();"
            "    throw new Error(`Status ${response.status}: ${errorText}`);"
            "  }"
            f"  return await response.{'json' if self.return_json else 'text'}();"
            "}"
        )
