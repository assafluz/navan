from pathlib import Path

from dotenv import load_dotenv

# Load repo-root .env before any code reads os.environ (e.g. REQRES_* in travelcorp.config).
load_dotenv(Path(__file__).resolve().parent / ".env")

import os

import pytest

pytest_plugins = ["pytest_playwright"]


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """Optional: PLAYWRIGHT_SLOW_MO=500 (milliseconds) to slow actions when using --headed."""
    raw = os.environ.get("PLAYWRIGHT_SLOW_MO", "").strip()
    if not raw:
        return browser_type_launch_args
    try:
        ms = int(raw)
    except ValueError:
        return browser_type_launch_args
    if ms <= 0:
        return browser_type_launch_args
    return {**browser_type_launch_args, "slow_mo": ms}
