"""
Corporate travel policy rules — pure functions only.

Kept separate from ``travelcorp.api`` so you can explain: HTTP client = transport;
this module = business wording the assignment asks to derive from the API response.
"""

from __future__ import annotations

from typing import Any, Mapping


def evaluate_policy(job: str | None) -> str:
    if job == "Manager":
        return "Business Class Allowed"
    if job == "Intern":
        return "Economy Only"
    return "Undefined Role"


def policy_line_for_job(job: str | None) -> str:
    """Human-readable line matching the assignment pseudocode."""
    if job == "Manager":
        return "Policy: Business Class Allowed"
    if job == "Intern":
        return "Policy: Economy Only"
    return f"Policy: Undefined Role ({job!r})"


def announce_policy_from_response_body(body: Mapping[str, Any]) -> str:
    """
    Decide from API JSON (simulated policy service), print, and return the line.
    Keeps transport (requests) separate from business wording.
    """
    job = body.get("job")
    line = policy_line_for_job(job if isinstance(job, str) else None)
    print(line)
    return line
