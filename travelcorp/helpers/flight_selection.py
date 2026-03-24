"""Parsing and selection logic for BlazeDemo flight results (not raw UI clicks)."""

from __future__ import annotations

from urllib.parse import parse_qs

from playwright.sync_api import Page


def parse_price(text: str) -> float:
    return float(text.replace("$", "").strip())


def select_lowest_price_flight(page: Page) -> tuple[str, float]:
    """
    Scan each results row, normalize prices, pick the minimum fare, submit that row,
    and verify the browser's POST to ``purchase.php`` carries the same flight id and
    price (the strongest end-to-end signal BlazeDemo exposes today).
    """
    rows = page.locator("table.table tbody tr")
    rows.first.wait_for(state="visible", timeout=30_000)
    count = rows.count()
    if count == 0:
        raise AssertionError("No flight rows found on reserve page.")

    lowest: float | None = None
    flight_number: str | None = None

    for i in range(count):
        row = rows.nth(i)
        price = parse_price(row.locator("td").nth(5).inner_text())
        number = row.locator("td").nth(1).inner_text().strip()
        if lowest is None or price < lowest:
            lowest = price
            flight_number = number

    assert flight_number is not None and lowest is not None

    chosen_row = page.locator("table.table tbody tr").filter(
        has=page.locator(f'input[name="flight"][value="{flight_number}"]')
    )
    if chosen_row.count() != 1:
        raise AssertionError(
            f"Could not resolve a unique row for flight {flight_number!r} "
            f"(matches={chosen_row.count()})."
        )

    with page.expect_request(
        lambda req: req.method == "POST" and req.url.rstrip("/").endswith("purchase.php")
    ) as post_req:
        with page.expect_navigation(wait_until="domcontentloaded"):
            chosen_row.locator("input[type='submit']").click()

    _assert_purchase_post_matches_selection(post_req.value.post_data, flight_number, lowest)
    return flight_number, lowest


def _assert_purchase_post_matches_selection(
    post_data: str | None, flight: str, price: float
) -> None:
    assert post_data, "Expected a POST body when choosing a flight."
    parsed = parse_qs(post_data)
    assert parsed.get("flight", [None])[0] == flight
    assert float(parsed.get("price", ["nan"])[0]) == price
