from __future__ import annotations

import requests

from travelcorp.config import REQRES_USERS_URL

_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def create_user(payload: dict, timeout: int = 30) -> requests.Response:
    return requests.post(
        REQRES_USERS_URL,
        json=payload,
        timeout=timeout,
        headers=_DEFAULT_HEADERS,
    )
