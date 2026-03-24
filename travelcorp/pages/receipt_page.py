from __future__ import annotations

import re

from playwright.sync_api import Page


class ReceiptPage:
    """Final BlazeDemo confirmation.php receipt table."""

    def __init__(self, page: Page) -> None:
        self._page = page

    def wait_for_loaded(self) -> None:
        self._page.wait_for_url("**/confirmation.php**")
        self._page.locator("table.table").wait_for()

    def purchase_id(self) -> str:
        return self._cell_for_row_label("Id")

    def amount_numeric(self) -> float:
        text = self._cell_for_row_label("Amount")
        match = re.search(r"[\d.]+", text)
        if not match:
            raise AssertionError(f"Could not parse amount from {text!r}")
        return float(match.group())

    def _cell_for_row_label(self, label: str) -> str:
        rows = self._page.locator("table.table tbody tr")
        for i in range(rows.count()):
            row = rows.nth(i)
            first = row.locator("td").nth(0).inner_text().strip()
            if first == label:
                return row.locator("td").nth(1).inner_text().strip()
        raise AssertionError(f"No receipt row found for label {label!r}")
