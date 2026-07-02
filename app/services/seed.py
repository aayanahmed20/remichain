from app import db
from app.models import Facility


DEMO_FACILITIES = [
    {"name": "Jinnah Community Clinic", "facility_type": "clinic", "city": "Lahore",
     "country": "Pakistan", "latitude": 31.5497, "longitude": 74.3436, "verified": True},
    {"name": "Green Valley Free Pharmacy", "facility_type": "pharmacy", "city": "Lahore",
     "country": "Pakistan", "latitude": 31.5204, "longitude": 74.3587, "verified": True},
    {"name": "Sindh Rural Health NGO", "facility_type": "ngo", "city": "Hyderabad",
     "country": "Pakistan", "latitude": 25.3960, "longitude": 68.3578, "verified": True},
    {"name": "Northern District Hospital", "facility_type": "hospital", "city": "Peshawar",
     "country": "Pakistan", "latitude": 34.0151, "longitude": 71.5249, "verified": True},
]


def seed_facilities():
    if Facility.query.first() is not None:
        return
    for data in DEMO_FACILITIES:
        db.session.add(Facility(**data))
    db.session.commit()
