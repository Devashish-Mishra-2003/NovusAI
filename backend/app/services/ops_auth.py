import time
import requests
from typing import Optional

OPS_TOKEN_URL = "https://ops.epo.org/3.2/auth/accesstoken"
USER_AGENT = "NovusAI/1.0 (contact: research@novusai.local)"

# Hardcoded for local development only – REMOVE/COMMENT BEFORE GIT PUSH!
_CONSUMER_KEY = "supersecretkey"
_CONSUMER_SECRET = "supersecretkey"

_access_token: Optional[str] = None
_token_expiry_ts: float = 0.0


def get_access_token() -> str:
    global _access_token, _token_expiry_ts

    now = time.time()
    if _access_token and now < _token_expiry_ts - 60:  # Refresh 1 min early
        return _access_token

    resp = requests.post(
        OPS_TOKEN_URL,
        auth=(_CONSUMER_KEY, _CONSUMER_SECRET),
        headers={
            "User-Agent": USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "client_credentials"},
        timeout=20,
    )
    resp.raise_for_status()

    data = resp.json()
    _access_token = data["access_token"]
    _token_expiry_ts = now + int(data.get("expires_in", 1200))  # Default 20 min
    return _access_token