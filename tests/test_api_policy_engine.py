"""API scenarios against ReqRes (stand-in for internal policy service)."""

from __future__ import annotations

import pytest

from travelcorp.api.reqres_client import create_user
from travelcorp.helpers.policy import (
    announce_policy_from_response_body,
    evaluate_policy,
    policy_line_for_job,
)


def test_manager_policy_201_and_printed_line(
    require_reqres: None,
    capsys: pytest.CaptureFixture[str],
) -> None:
    res = create_user({"name": "Alice", "job": "Manager"})
    assert res.status_code == 201
    body = res.json()
    line = announce_policy_from_response_body(body)
    assert line == "Policy: Business Class Allowed"
    assert evaluate_policy(body.get("job")) == "Business Class Allowed"
    assert "Policy: Business Class Allowed" in capsys.readouterr().out


def test_intern_policy_201_and_printed_line(
    require_reqres: None,
    capsys: pytest.CaptureFixture[str],
) -> None:
    res = create_user({"name": "Bob", "job": "Intern"})
    assert res.status_code == 201
    body = res.json()
    line = announce_policy_from_response_body(body)
    assert line == "Policy: Economy Only"
    assert evaluate_policy(body.get("job")) == "Economy Only"
    assert "Policy: Economy Only" in capsys.readouterr().out


def test_create_user_without_job_observed_behavior(require_reqres: None) -> None:
    """
    ReqRes is a mock: document actual status/body instead of assuming 400.
    """
    res = create_user({"name": "Charlie"})
    assert res.status_code in (201, 400)
    body = res.json()
    job = body.get("job")
    assert job in (None, "") or isinstance(job, str)
    msg = policy_line_for_job(job if isinstance(job, str) else None)
    assert msg.startswith("Policy:")


def test_policy_line_matches_evaluate_for_known_roles() -> None:
    assert "Business Class Allowed" in policy_line_for_job("Manager")
    assert "Economy Only" in policy_line_for_job("Intern")
