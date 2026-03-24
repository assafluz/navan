# TravelCorp Booking Engine — automation design & architecture

This document maps the assignment to the implementation, records the layered architecture, and includes the key code excerpts reviewers asked for.

## Requirement traceability

| Assignment requirement | Implementation response |
| --- | --- |
| Navigate to the homepage and select departure city Boston and destination London | UI flow opens BlazeDemo, selects Boston and London, submits **Find Flights** (`travelcorp/pages/home_page.py`). |
| Do not click the first result. Write a function to find the flight with the lowest price and click the matching **Choose This Flight** button | `select_lowest_price_flight` in `travelcorp/helpers/flight_selection.py` scans rows, parses prices, picks the minimum, clicks the matching control, and asserts the **POST** to `purchase.php` carries the same `flight` and `price`. |
| Store the Flight Number and Price into variables | After navigation to the **confirmation-of-selection** screen (`purchase.php`), the test reads **Flight Number** and **Price** from the on-page summary into `flight_number` and `price_on_confirmation_screen` (`tests/test_ui_booking_flow.py`, `PurchasePage`). |
| Fill out the passenger details and click **Purchase Flight** | `PurchasePage.fill_mock_passenger_details` + `purchase_flight` (`travelcorp/pages/purchase_page.py`). |
| Verify that the Id is generated and the Amount matches the selected price | **Id**: asserted non-empty. **Amount**: when the sandbox renders a summary that **matches** the chosen row (and the POST body), we assert `final_amount == price_on_confirmation_screen` (assignment intent). When BlazeDemo serves its known **static** template (summary/receipt ignore POST), that strict equality cannot hold; the test keeps **POST verification** inside `select_lowest_price_flight` and falls back to “booking completed” checks (`final_amount > 0`). See **Sandbox note** below. |
| Create a user with job title Manager using payload `{ "name": "Alice", "job": "Manager" }` | `create_user` + test asserts HTTP 201 (`tests/test_api_policy_engine.py`). |
| Create a user with job title Intern using payload `{ "name": "Bob", "job": "Intern" }` | Same, with Intern payload and 201. |
| Write a function that makes a decision based on the response: Manager → Business Class Allowed, Intern → Economy Only | `evaluate_policy` / `policy_line_for_job` / `announce_policy_from_response_body` (`travelcorp/helpers/policy.py`). |
| Negative test: create user without a job title and assert how the system handles it | Payload without `job`; asserts status is an allowed code and documents body shape without assuming production error contracts (ReqRes is a mock). |

## Short technical summary

The solution is treated as a **small automation product**, not a one-off script.

**UI coverage**

- End-to-end booking flow  
- Dynamic selection (lowest price)  
- Data consistency where the sandbox allows it (POST body vs chosen row)

**API coverage**

- Request handling and status codes  
- Business rule wording separated from transport  
- Negative / ambiguous input behavior on a mock service

**Layering**

- **UI interaction**: `travelcorp/pages/`  
- **API interaction**: `travelcorp/api/`  
- **Helpers**: parsing, selection, policy strings — `travelcorp/helpers/`

## Sandbox note (BlazeDemo)

Observed March 2026: a correct `POST` to `https://blazedemo.com/purchase.php` (e.g. `flight=9696&price=200.98&airline=Aer+Lingus&fromPort=Boston&toPort=London`) still returns the static **TLV → SFO / UA954** template in HTML. The automation **intercepts and asserts that POST** so the lowest-price decision is still proven end-to-end from the browser.

## Code snippets

### Lowest price selection (concept)

```python
def parse_price(text):
    return float(text.replace("$", "").strip())


def select_lowest_price(page):
    rows = page.locator("table tbody tr").all()

    lowest = None
    chosen = None
    flight_number = None

    for row in rows:
        price = parse_price(row.locator("td").nth(5).inner_text())
        number = row.locator("td").nth(1).inner_text()

        if lowest is None or price < lowest:
            lowest = price
            chosen = row
            flight_number = number

    chosen.locator("input[type='submit']").click()

    return flight_number, lowest
```

The shipped helper adds **row resolution via the hidden `flight` field** (BlazeDemo’s invalid `<tr><form>` markup) and **POST verification**; see `travelcorp/helpers/flight_selection.py` for the authoritative version.

### Final booking validation (concept)

```python
def test_booking_flow():
    home.open()
    home.search_flights("Boston", "London")

    flight_number, selected_price = select_lowest_price(page)

    purchase.fill_details()
    purchase.submit()

    purchase_id = purchase.get_id()
    final_amount = purchase.get_amount()

    assert purchase_id.strip() != ""
    assert final_amount == selected_price
```

The repository test names steps explicitly, reads **flight/price from the purchase-page confirmation summary**, and when that summary matches the chosen itinerary asserts **`final_amount == price_on_confirmation_screen`**. If BlazeDemo serves static copy, the test relies on **POST verification** in `select_lowest_price_flight` plus receipt sanity checks. See `tests/test_ui_booking_flow.py`.

### Policy logic

```python
def evaluate_policy(job):
    if job == "Manager":
        return "Business Class Allowed"
    if job == "Intern":
        return "Economy Only"
```

See `travelcorp/helpers/policy.py` for printable lines matching the assignment pseudocode.

### API validation (concept)

```python
def test_policy():
    res = requests.post(URL, json={"name": "Alice", "job": "Manager"})
    assert res.status_code == 201
    assert evaluate_policy("Manager") == "Business Class Allowed"

    res = requests.post(URL, json={"name": "Bob", "job": "Intern"})
    assert res.status_code == 201
    assert evaluate_policy("Intern") == "Economy Only"
```

### Negative case

```python
def test_missing_job():
    res = requests.post(URL, json={"name": "Charlie"})
    assert res.status_code in [201, 400]
```

ReqRes may still return **201** without `job`; the project test records **observed** behavior instead of hard-coding a fictional production contract.
