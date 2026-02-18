from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class StoredAuth(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    cookies: Optional[List[Any]] = None
    # Add this to store the captured x-trader-client and other headers
    headers: Optional[Dict[str, str]] = None

    model_config = ConfigDict(extra="ignore")
