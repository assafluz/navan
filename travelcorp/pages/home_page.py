from __future__ import annotations

from playwright.sync_api import Page

from travelcorp.config import BLAZE_DEMO_BASE


class HomePage:
    def __init__(self, page: Page) -> None:
        self._page = page

    def open(self) -> None:
        self._page.goto(f"{BLAZE_DEMO_BASE}/", wait_until="domcontentloaded")

    def search_flights(self, departure_city: str, destination_city: str) -> None:
        self._page.locator('select[name="fromPort"]').select_option(label=departure_city)
        self._page.locator('select[name="toPort"]').select_option(label=destination_city)
        self._page.get_by_role("button", name="Find Flights").click()
        self._page.wait_for_url("**/reserve.php**")
