<div align="center">

# RemiChain

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=22&duration=3000&pause=1000&color=0F766E&center=true&vCenter=true&width=700&lines=Connecting+Surplus+Medical+Supplies+to+Need;Built+for+SDG+3%3A+Good+Health+%26+Well-Being;Urgency-Aware+Donation+Matching+Engine;Reducing+Medical+Waste%2C+Closing+Access+Gaps" />

<br>

<a href="https://github.com/aayanahmed20/remichain">
  <img src="https://img.shields.io/badge/Project-RemiChain-0d1117?style=for-the-badge&logo=github&logoColor=0F766E"/>
</a>
<a href="https://github.com/aayanahmed20">
  <img src="https://img.shields.io/badge/Developer-Aayan%20Ahmed-0d1117?style=for-the-badge&logo=github&logoColor=white"/>
</a>
<a href="#">
  <img src="https://img.shields.io/badge/SDG-3%20Good%20Health-0d1117?style=for-the-badge&logo=un&logoColor=orange"/>
</a>

</div>

---

## Overview

RemiChain is a **surplus-to-need matching platform** for medical supplies. Clinics, pharmacies,
hospitals, and NGOs routinely discard usable medication, PPE, and equipment while nearby facilities
run short of the exact same items. RemiChain gives every facility a place to list what it has too much
of and what it's short on, then runs a transparent scoring engine that proposes the best pairing —
weighing **urgency, expiry, distance, and quantity fit** — before supplies go to waste.

It is built directly against **UN Sustainable Development Goal 3 (Good Health and Well-being)**,
targeting the gap between medical resource surplus and medical resource scarcity.

---

## Purpose

RemiChain is built to explore:

- Resource-matching algorithms for humanitarian logistics
- Reducing expired/wasted medical inventory through timely redistribution
- Equitable prioritization (critical-need facilities surface first, not just first-come-first-served)
- Lightweight, self-hostable tools for clinics and NGOs with limited IT budgets
- Transparent, auditable matching logic — no black-box scoring

---

## Key Features

- Facility registry for hospitals, clinics, pharmacies, and NGOs
- Surplus donation listings with category, quantity, condition, and expiry tracking
- Need requests with configurable urgency levels (low → critical)
- Weighted matching engine combining urgency, expiry pressure, geographic proximity, and quantity coverage
- Automatic match proposal the moment a new request is posted
- Batch matching pass endpoint for periodically re-scanning open requests
- REST API for donations, requests, and matches
- Lightweight dashboard for tracking live donations, requests, and proposed matches
- Zero external dependencies beyond Flask + SQLite — runs anywhere

---

## System Architecture

```
Donor Facility          Recipient Facility
      │                         │
      ▼                         ▼
 List Donation             Post Request
      │                         │
      └──────────┬──────────────┘
                  ▼
          Matching Engine
   (urgency · expiry · distance · quantity)
                  │
                  ▼
          Proposed Match
                  │
                  ▼
        Dashboard / REST API
```

---

## Matching Engine

Every donation-request pair of the same item is scored as:

```
score = (URGENCY_WEIGHT   × urgency_score)
      + (EXPIRY_WEIGHT    × expiry_urgency)
      + (PROXIMITY_WEIGHT × proximity_score)
      + (QUANTITY_WEIGHT  × coverage_ratio)
```

- **urgency_score** — normalized from the requester's declared urgency (low → critical)
- **expiry_urgency** — items expiring within 14 days score highest; already-expired stock is disqualified
- **proximity_score** — haversine distance between donor and recipient, closer scores higher
- **coverage_ratio** — how much of the requested quantity the donation can actually fulfill

Weights live in `config.py` so the prioritization logic can be tuned without touching the algorithm.

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/aayanahmed20/remichain.git
cd remichain
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
python run.py
```

The app starts at `http://localhost:5000` with a few demo facilities pre-seeded so you can
list a donation and post a request immediately.

### Run tests

```bash
pytest
```

---

## Project Structure

```
remichain/
├── app/
│   ├── models/          # Facility, SupplyDonation, SupplyRequest, Match
│   ├── routes/          # main, donations, requests, api blueprints
│   └── services/        # matching engine + demo data seeding
├── templates/            # Jinja2 templates (dashboard, donate, request forms)
├── static/css/           # stylesheet
├── tests/                 # pytest suite for the matching engine
├── config.py
├── run.py
└── requirements.txt
```

---

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/donations` | GET | List all donations |
| `/api/requests` | GET | List all requests |
| `/api/matches` | GET | List all proposed/confirmed matches |
| `/api/requests/<id>/candidates` | GET | Top-ranked donation candidates for a request |
| `/api/run-matching` | POST | Run a full matching pass over all open requests |

---

## Roadmap

- [ ] SMS/WhatsApp notifications for facilities without reliable internet
- [ ] Multi-language interface (Urdu, Arabic, French)
- [ ] Cold-chain flag for temperature-sensitive medication
- [ ] Facility verification workflow

---

<div align="center">
Built for the <b>Readme Generation Hackathon</b> — SDG 3: Good Health and Well-being
</div>
