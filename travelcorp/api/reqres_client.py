from __future__ import annotations

import os

import requests

from travelcorp.config import REQRES_USERS_URL

_BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def reqres_request_headers(*, json_body: bool = False) -> dict[str, str]:
    """
    ReqRes may require ``x-api-key`` (see app dashboard). Free keys:
    https://app.reqres.in/api-keys
    """
    headers: dict[str, str] = {
        "User-Agent": _BROWSER_UA,
        "Accept": "application/json",
    }
    if json_body:
        headers["Content-Type"] = "application/json"
    key = os.environ.get("REQRES_API_KEY", "").strip()
    if key:
        headers["x-api-key"] = key
    return headers


def create_user(payload: dict, timeout: int = 30) -> requests.Response:
    """POST stand-in for creating a traveler profile (assignment Part 2)."""
    return requests.post(
        REQRES_USERS_URL,
        json=payload,
        timeout=timeout,
        headers=reqres_request_headers(json_body=True),
    )
