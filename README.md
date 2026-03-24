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
- Network access to `https://blazedemo.com` (UI) and `https://reqres.in` (API; some corporate networks return HTTP 403)

## Setup and run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
pytest
```

API tests skip automatically if ReqRes is unreachable from your network.

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
