# TravelCorp Booking Engine — automation exercise

Concise take-home solution: **Playwright (Python)** for the BlazeDemo booking flow and **requests** for ReqRes-based “policy API” scenarios. The goal is readable structure, explicit business logic, and requirements you can trace from spec to code.

## Executive summary

- **UI**: End-to-end search → lowest-fare selection (not “click first row”) → checkout → receipt checks, with page objects and a dedicated selection helper.
- **API**: ReqRes `POST /api/users` stands in for traveler onboarding; policy wording is isolated from HTTP so rules stay easy to review and extend.
- **Design detail**: BlazeDemo’s HTML response for `purchase.php` / `confirmation.php` is effectively **static** (POST bodies are correct, but rendered copy does not reflect the chosen fare). The automation therefore **asserts the outbound POST** after flight selection and validates **receipt Id** plus a sane charged amount. See [AUTOMATION_DESIGN.md](AUTOMATION_DESIGN.md).

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
