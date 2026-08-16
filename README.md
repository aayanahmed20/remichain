# RemiChain

RemiChain matches surplus medical supplies with facilities that need them, helping usable equipment and medication move from storage to care settings before they expire. It is an open-source donation-and-matching prototype intended for research and small-scale deployments.

RemiChain received an honorable mention in the GitHub README Generation Hackathon hosted by Present Me Academy (selected from 480+ participants).

## Quickstart

1. Clone the repository:

   git clone https://github.com/aayanahmed20/remichain.git
   cd remichain

2. Create and activate a Python virtual environment, then install requirements:

   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .\.venv\Scripts\activate    # Windows
   pip install -r requirements.txt

3. Initialize the database (SQLite by default) and start the server:

   export FLASK_APP=app
   export FLASK_ENV=development
   flask run

   The app will be available at http://127.0.0.1:5000

## Overview

- Facilities can list surplus supplies as donations (quantity, category, expiry date).
- Facilities can submit requests for supplies; each request receives an urgency score.
- A matching engine scores potential donation→request pairs and proposes high-quality matches.
- A dashboard displays recent donations, requests, and matched proposals.

## Architecture & Tech Stack

- Python 3.10+
- Flask
- Flask-SQLAlchemy (SQLite by default)
- pytest for unit tests

Project structure (important folders):

- `app/models/` — ORM models (Facility, SupplyDonation, SupplyRequest, Match)
- `app/routes/` — web routes and JSON API endpoints
- `app/services/matching.py` — matching and scoring logic
- `app/services/seed.py` — seed data used on first run
- `tests/` — test suite for the matching engine

## API Endpoints (examples)

- `GET /api/donations` — list donations
- `GET /api/requests` — list requests
- `GET /api/matches` — list proposed matches
- `POST /api/run-matching` — trigger a matching pass

## Running tests

Run the matching engine unit tests:

   pytest -q

## Contributing

Contributions are welcome. Please open issues for bugs or enhancement requests and submit pull requests with clear descriptions and tests where appropriate. Keep changes focused and avoid unrelated formatting edits.

## Security & Data

- This project uses SQLite by default for local development. Do not commit production secrets or large data files to the repository.
- If you find a security issue, open a private issue describing the problem and remediation steps.

## License

This project is provided under the MIT License. See `LICENSE` for details.
