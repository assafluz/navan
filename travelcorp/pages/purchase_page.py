from __future__ import annotations

import re

from playwright.sync_api import Page


class PurchasePage:
    """Checkout form on purchase.php (after a flight is chosen)."""

    def __init__(self, page: Page) -> None:
        self._page = page

    def wait_for_loaded(self) -> None:
        self._page.wait_for_url("**/purchase.php**")
        self._page.get_by_role("heading", name=re.compile("reserved", re.I)).wait_for()

    def summary_flight_number(self) -> str:
        return self._value_after_label("Flight Number")

    def summary_price(self) -> float:
        return float(self._value_after_label("Price"))

    def fill_mock_passenger_details(self) -> None:
        p = self._page
        p.locator("#inputName").fill("Alex Tester")
        p.locator("#address").fill("1 Test Street")
        p.locator("#city").fill("Boston")
        p.locator("#state").fill("MA")
        p.locator("#zipCode").fill("02108")
        p.locator("#creditCardNumber").fill("4111111111111111")
        p.locator("#creditCardMonth").fill("12")
        p.locator("#creditCardYear").fill("2030")
        p.locator("#nameOnCard").fill("Alex Tester")

    def purchase_flight(self) -> None:
        self._page.get_by_role("button", name="Purchase Flight").click()
        self._page.wait_for_url("**/confirmation.php**")

    def _value_after_label(self, label: str) -> str:
        para = self._page.locator("p", has_text=re.compile(rf"^{label}:", re.I))
        text = para.inner_text()
        return text.split(":", 1)[1].strip()
