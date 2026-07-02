"""
Matching engine for RemiChain.

Pairs surplus medical supply donations with open requests using a weighted
score built from:
  - urgency of the requesting facility
  - how soon the donated item expires (use-it-or-lose-it priority)
  - geographic proximity between donor and recipient
  - how well the offered quantity covers the need

This is intentionally readable over clever: hackathon judges and future
contributors should be able to follow the scoring logic without a math degree.
"""

from datetime import date
from math import radians, sin, cos, sqrt, atan2

from flask import current_app

from app import db
from app.models import SupplyDonation, SupplyRequest, Match


def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance between two lat/lon points, in kilometers."""
    if None in (lat1, lon1, lat2, lon2):
        return None

    R = 6371.0
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)

    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    return 2 * R * atan2(sqrt(a), sqrt(1 - a))


def _expiry_urgency(donation):
    """Higher score = the donated item needs to move soon (or never expires)."""
    if donation.expiry_date is None:
        return 0.5  # durable equipment: mild priority, no rush
    days_left = (donation.expiry_date - date.today()).days
    if days_left <= 0:
        return 0.0  # already expired, should not be matched
    if days_left <= 14:
        return 1.0
    if days_left <= 60:
        return 0.6
    return 0.3


def _proximity_score(donation, req):
    donor = donation.facility
    recipient = req.facility
    dist = haversine_km(donor.latitude, donor.longitude, recipient.latitude, recipient.longitude)
    if dist is None:
        return 0.3  # unknown location: neutral-low score
    if dist <= 25:
        return 1.0
    if dist <= 100:
        return 0.7
    if dist <= 500:
        return 0.4
    return 0.15


def score_pair(donation: SupplyDonation, req: SupplyRequest, cfg) -> float:
    """Weighted score for how good a donation-to-request match is. Higher is better."""
    if donation.item_name.strip().lower() != req.item_name.strip().lower():
        return -1.0  # not the same item at all
    if donation.expiry_date and donation.expiry_date <= date.today():
        return -1.0  # never match expired stock

    urgency = req.urgency_score / 4.0  # normalize 0-1
    expiry = _expiry_urgency(donation)
    proximity = _proximity_score(donation, req)
    coverage = min(donation.quantity / req.quantity_needed, 1.0)

    return (
        cfg.get("URGENCY_WEIGHT", 3.0) * urgency
        + cfg.get("EXPIRY_WEIGHT", 2.0) * expiry
        + cfg.get("PROXIMITY_WEIGHT", 1.5) * proximity
        + cfg.get("QUANTITY_WEIGHT", 1.0) * coverage
    )


def find_matches_for_request(req: SupplyRequest, limit=5):
    """Return the best-scoring available donations for a given request."""
    candidates = SupplyDonation.query.filter_by(status="available").all()
    cfg = current_app.config
    scored = [(d, score_pair(d, req, cfg)) for d in candidates]
    scored = [(d, s) for d, s in scored if s > 0]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:limit]


def create_match(donation: SupplyDonation, req: SupplyRequest, score: float):
    matched_qty = min(donation.quantity, req.quantity_needed)
    match = Match(
        donation_id=donation.id,
        request_id=req.id,
        score=score,
        matched_quantity=matched_qty,
        status="proposed",
    )
    db.session.add(match)
    db.session.commit()
    return match


def run_matching_pass():
    """Batch job: scan every open request and propose the best match, if any."""
    created = []
    open_requests = SupplyRequest.query.filter(
        SupplyRequest.status.in_(["open", "partially_fulfilled"])
    ).all()

    for req in open_requests:
        best = find_matches_for_request(req, limit=1)
        if best:
            donation, score = best[0]
            created.append(create_match(donation, req, score))

    return created
