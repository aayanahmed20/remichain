# RemiChain

RemiChain matches surplus medical supplies with the facilities that need them, instead of letting usable equipment and medication expire in storage while other clinics run short. It started as a hackathon project.

## Why this exists

Hospitals and clinics regularly end up with supplies they can't use in time - equipment nobody needs right now, medication approaching its expiry date - while other facilities nearby are short on exactly that. RemiChain is a small matching system that tries to close that gap automatically instead of relying on someone noticing and making a few phone calls.

## How the matching works

Facilities list surplus supplies as donations and log what they need as requests. A matching engine (`app/services/matching.py`) scores every possible donation-to-request pair using four factors: how urgent the request is, how soon the donated item expires, how close the donor and recipient are geographically, and how much of the requested quantity the donation would cover. The weights for each factor are configurable in `config.py`, and the scoring logic is kept simple and readable on purpose rather than clever.

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

## Getting started

```bash
pip install -r requirements.txt
python run.py
```

Then open `http://localhost:5000`. The app creates its SQLite database and seeds a few sample facilities automatically on first run.

## Project structure

- `app/models/` - Facility, SupplyDonation, SupplyRequest, Match
- `app/routes/` - main pages, donation/request forms, JSON API
- `app/services/matching.py` - the scoring and matching logic
- `app/services/seed.py` - sample facility data used on first run
- `tests/test_matching.py` - tests for the matching engine

## Status

The core matching logic and the donate/request/dashboard flow work end to end. There's no authentication yet, so right now anyone can list a donation or request on behalf of any facility - that's the next thing I'd want to fix before this went anywhere near real use.
