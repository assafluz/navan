from __future__ import annotations

import pytest
import requests


@pytest.fixture(scope="session")
def reqres_reachable() -> bool:
    try:
        r = requests.get(
            "https://reqres.in/api/users?page=1",
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
            },
        )
    except requests.RequestException:
        return False
    return r.status_code == 200


@pytest.fixture
def require_reqres(reqres_reachable: bool) -> None:
    if not reqres_reachable:
        pytest.skip("ReqRes is not reachable from this network (needed for API tests).")
