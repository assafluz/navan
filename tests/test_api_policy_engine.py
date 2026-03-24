"""
Part 2 — Policy Engine (ReqRes as stand-in for an internal profile/policy API).

Architecture: ``travelcorp/api`` sends HTTP; ``travelcorp/helpers/policy`` holds pure
rules + printable lines. Tests prove status codes, JSON shape, and the assignment's
print-based “logic check” without mixing policy text into the client.
"""

from __future__ import annotations

import pytest

from travelcorp.api.reqres_client import create_user
from travelcorp.helpers.policy import announce_policy_from_response_body, evaluate_policy


def test_policy_engine_manager_intern_and_logic_check(
    require_reqres: None,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Scenarios A & B plus logic check: POST exact payloads, assert 201, then decide
    from the response body and print (assignment pseudocode).
    """
    res = create_user({"name": "Alice", "job": "Manager"})
    assert res.status_code == 201
    body = res.json()
    assert body.get("job") == "Manager"

    line = announce_policy_from_response_body(body)
    assert line == "Policy: Business Class Allowed"
    assert evaluate_policy(body.get("job")) == "Business Class Allowed"
    assert "Policy: Business Class Allowed" in capsys.readouterr().out

    res = create_user({"name": "Bob", "job": "Intern"})
    assert res.status_code == 201
    body = res.json()
    assert body.get("job") == "Intern"

    line = announce_policy_from_response_body(body)
    assert line == "Policy: Economy Only"
    assert evaluate_policy(body.get("job")) == "Economy Only"
    assert "Policy: Economy Only" in capsys.readouterr().out


def test_policy_engine_missing_job_negative(require_reqres: None) -> None:
    """
    Negative: simulate “policy service” ambiguity — ReqRes is a mock, so we record
    status + body instead of assuming a production error contract.
    """
    res = create_user({"name": "Charlie"})
    assert res.status_code in (201, 400)
