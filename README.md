# TravelCorp Booking Engine — automation exercise

Concise take-home solution: **Playwright (Python)** for the BlazeDemo booking flow and **requests** for ReqRes-based “policy API” scenarios. The goal is readable structure, explicit business logic, and requirements you can trace from spec to code.

## Executive summary

- **UI**: Assignment Part 1 in order: Boston → London search → **lowest-price** selection function → **flight/price read from the purchase-page confirmation summary** → mock checkout → receipt **Id** and **Amount** (strict `Amount ==` confirmation price when the UI matches the POST; otherwise POST is asserted in the helper and receipt checks stay realistic for the static sandbox). See [AUTOMATION_DESIGN.md](AUTOMATION_DESIGN.md).
- **API**: ReqRes `POST /api/users` stands in for traveler onboarding; policy wording is isolated from HTTP so rules stay easy to review and extend.

## Repository layout

| Path | Role |
| --- | --- |
| `travelcorp/pages/` | UI interaction layer (home, purchase, receipt) |
| `travelcorp/helpers/` | Lowest-price logic, policy strings |
| `travelcorp/api/` | Thin ReqRes client |
| `tests/` | Pytest UI + API specs |
| [AUTOMATION_DESIGN.md](AUTOMATION_DESIGN.md) | Requirement traceability, architecture, snippets |

## Prerequisites

- Python 3.9+
- Network access to `https://blazedemo.com` (UI)
- **ReqRes API**: [ReqRes](https://reqres.in/) may require an **`x-api-key`** for `/api/users` (JSON error `missing_api_key` in the browser means you need a key). Create a free key at [app.reqres.in/api-keys](https://app.reqres.in/api-keys), then:

```bash
export REQRES_API_KEY="your_key_here"
pytest tests/test_api_policy_engine.py -v -s
```

Optional: `REQRES_USERS_URL` if your project uses a different base URL (see [ReqRes docs](https://app.reqres.in/docs#authentication)).

## Setup and run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
cp .env.example .env
# Edit .env — set REQRES_API_KEY from https://app.reqres.in/api-keys
pytest
```

Pytest loads `.env` from the repo root automatically (via `python-dotenv` in `conftest.py`). **Do not commit `.env`** — it is listed in `.gitignore`; only `.env.example` is tracked.

### API tests only (see printed policy lines)

```bash
pytest tests/test_api_policy_engine.py -v -s
```

`-s` shows the assignment’s `print` output. Tests **skip** if ReqRes does not return usable responses (set `REQRES_API_KEY` if you see `missing_api_key`).

### UI in a visible browser (optional slow motion)

```bash
pytest tests/test_ui_booking_flow.py -v --headed
PLAYWRIGHT_SLOW_MO=400 pytest tests/test_ui_booking_flow.py -v --headed
```

API tests skip when ReqRes is unreachable, blocked, or when **`REQRES_API_KEY`** is missing but the host requires it.

## Publishing to Git

```bash
git init
git add .
git commit -m "Add TravelCorp BlazeDemo + ReqRes automation exercise"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

Replace `<your-repo-url>` with your hosting URL (for example `https://github.com/<you>/travelcorp-booking-engine.git`).
