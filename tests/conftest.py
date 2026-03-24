from __future__ import annotations

import pytest
import requests

from travelcorp.api.reqres_client import reqres_request_headers
from travelcorp.config import REQRES_USERS_URL


@pytest.fixture(scope="session")
def reqres_reachable() -> bool:
    """
    ReqRes may require ``REQRES_API_KEY`` (browser GET to /api/users can return JSON
    ``missing_api_key`` without it). Probes GET then POST with the same headers as tests.
    """
    try:
        r = requests.get(
            f"{REQRES_USERS_URL}?page=1",
            timeout=15,
            headers=reqres_request_headers(),
        )
        if r.status_code == 200:
            return True
    except requests.RequestException:
        pass

    try:
        r = requests.post(
            REQRES_USERS_URL,
            json={"name": "probe", "job": "probe"},
            timeout=15,
            headers=reqres_request_headers(json_body=True),
        )
        return r.status_code == 201
    except requests.RequestException:
        return False


@pytest.fixture
def require_reqres(reqres_reachable: bool) -> None:
    if not reqres_reachable:
        pytest.skip(
            "ReqRes API not working from this environment. "
            "Create a free key at https://app.reqres.in/api-keys and run with: "
            "export REQRES_API_KEY='your_key'"
        )
