"""Happy-path UI automation: BlazeDemo booking with lowest-price selection."""

from __future__ import annotations

from playwright.sync_api import Page

from travelcorp.helpers.flight_selection import select_lowest_price_flight
from travelcorp.pages import HomePage, PurchasePage, ReceiptPage


def test_booking_happy_path_lowest_price_and_receipt(page: Page) -> None:
    """
    End-to-end flow with deliberate logic (not first-row click):

    - Search Boston → London.
    - Pick the numerically lowest fare; the helper also asserts the outbound POST
      matches that choice (see ``AUTOMATION_DESIGN.md`` for sandbox HTML caveats).
    - Complete checkout and validate a booking Id on the receipt.
    """
    home = HomePage(page)
    home.open()
    home.search_flights("Boston", "London")

    flight_from_table, selected_price = select_lowest_price_flight(page)
    stored_flight_number = flight_from_table
    stored_ticket_price = selected_price

    purchase = PurchasePage(page)
    purchase.wait_for_loaded()

    purchase.fill_mock_passenger_details()
    purchase.purchase_flight()

    receipt = ReceiptPage(page)
    receipt.wait_for_loaded()

    purchase_id = receipt.purchase_id()
    final_amount = receipt.amount_numeric()

    assert purchase_id.strip() != ""
    assert stored_flight_number
    assert stored_ticket_price > 0
    assert final_amount > 0
