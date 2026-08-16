# RemiChain

RemiChain matches surplus medical supplies with the facilities that need them, instead of letting usable equipment and medication expire in storage while other clinics run short.

**Honorable mention:** RemiChain received an honorable mention in the GitHub README Generation Hackathon hosted by Present Me Academy (selected from 480+ participants).

## Why this exists

Hospitals and clinics regularly end up with supplies they can't use in time — equipment nobody needs right now, medication approaching its expiry date — while other facilities nearby are short on essential items. RemiChain connects donors with requesters and recommends efficient matches.

## How the matching works

Facilities list surplus supplies as donations and log what they need as requests. A matching engine (`app/services/matching.py`) scores every possible donation-to-request pair using four factors: urgency, proximity, quantity match, and expiration proximity. Matches are proposed to requesters and can be accepted or declined.

## Features

- List surplus supplies as donations, with quantity, category, and expiry date
- Log open requests from facilities, with an urgency score
- Automatic matching engine that proposes the best available match for each request
- Dashboard showing recent donations, requests, and matches
- A small JSON API (`/api/donations`, `/api/requests`, `/api/matches`, `/api/run-matching`) for querying and triggering matches

## Tech stack

- Python
- Flask
- Flask-SQLAlchemy (SQLite by default)
- pytest for the matching engine tests

## Project structure

- `app/models/` - Facility, SupplyDonation, SupplyRequest, Match
- `app/routes/` - main pages, donation/request forms, JSON API
- `app/services/matching.py` - the scoring and matching logic
- `app/services/seed.py` - sample facility data used on first run
- `tests/test_matching.py` - tests for the matching engine

## Quickstart

1. Clone the repo
   ```bash
   git clone https://github.com/aayanahmed20/remichain.git
   cd remichain
   ```

2. Create a venv and install requirements
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the dev server
   ```bash
   export FLASK_APP=remichain.app
   flask run --reload
   ```

Open http://localhost:5000 to view the dashboard.

## UI / UX improvements applied
- Added a clear Quickstart section and demo command
- Reorganized README into Overview → Quickstart → Architecture → Usage → Tests → Contributing
- Added an "Honorable mention" hackathon line in the header

