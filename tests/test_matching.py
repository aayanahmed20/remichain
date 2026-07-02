import os
import sys
from datetime import date, timedelta

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models import Facility, SupplyDonation, SupplyRequest
from app.services.matching import score_pair, find_matches_for_request


@pytest.fixture
def app():
    class TestConfig:
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SECRET_KEY = "test"
        URGENCY_WEIGHT = 3.0
        EXPIRY_WEIGHT = 2.0
        PROXIMITY_WEIGHT = 1.5
        QUANTITY_WEIGHT = 1.0

    app = create_app(TestConfig)
    yield app


@pytest.fixture
def facilities(app):
    with app.app_context():
        donor = Facility(name="Donor Clinic", facility_type="clinic", city="Lahore",
                          country="Pakistan", latitude=31.55, longitude=74.34)
        recipient = Facility(name="Rural NGO", facility_type="ngo", city="Lahore",
                              country="Pakistan", latitude=31.56, longitude=74.35)
        db.session.add_all([donor, recipient])
        db.session.commit()
        return donor.id, recipient.id


def test_matching_item_names_must_align(app, facilities):
    donor_id, recipient_id = facilities
    with app.app_context():
        donation = SupplyDonation(facility_id=donor_id, item_name="Amoxicillin",
                                   category="medication", quantity=100,
                                   expiry_date=date.today() + timedelta(days=30))
        req = SupplyRequest(facility_id=recipient_id, item_name="Paracetamol",
                             category="medication", quantity_needed=50, urgency="high")
        assert score_pair(donation, req, app.config) == -1.0


def test_expired_donation_never_matches(app, facilities):
    donor_id, recipient_id = facilities
    with app.app_context():
        donation = SupplyDonation(facility_id=donor_id, item_name="Amoxicillin",
                                   category="medication", quantity=100,
                                   expiry_date=date.today() - timedelta(days=1))
        req = SupplyRequest(facility_id=recipient_id, item_name="Amoxicillin",
                             category="medication", quantity_needed=50, urgency="high")
        assert score_pair(donation, req, app.config) == -1.0


def test_high_urgency_and_near_expiry_scores_highly(app, facilities):
    donor_id, recipient_id = facilities
    with app.app_context():
        donation = SupplyDonation(facility_id=donor_id, item_name="Amoxicillin",
                                   category="medication", quantity=100,
                                   expiry_date=date.today() + timedelta(days=10))
        req_critical = SupplyRequest(facility_id=recipient_id, item_name="Amoxicillin",
                                      category="medication", quantity_needed=50, urgency="critical")
        req_low = SupplyRequest(facility_id=recipient_id, item_name="Amoxicillin",
                                 category="medication", quantity_needed=50, urgency="low")

        score_critical = score_pair(donation, req_critical, app.config)
        score_low = score_pair(donation, req_low, app.config)
        assert score_critical > score_low


def test_find_matches_for_request_returns_ranked_results(app, facilities):
    donor_id, recipient_id = facilities
    with app.app_context():
        d1 = SupplyDonation(facility_id=donor_id, item_name="Amoxicillin", category="medication",
                             quantity=100, expiry_date=date.today() + timedelta(days=5))
        d2 = SupplyDonation(facility_id=donor_id, item_name="Amoxicillin", category="medication",
                             quantity=10, expiry_date=date.today() + timedelta(days=300))
        req = SupplyRequest(facility_id=recipient_id, item_name="Amoxicillin",
                             category="medication", quantity_needed=100, urgency="high")
        db.session.add_all([d1, d2, req])
        db.session.commit()

        results = find_matches_for_request(req)
        assert len(results) == 2
        assert results[0][1] >= results[1][1]  # sorted descending by score
