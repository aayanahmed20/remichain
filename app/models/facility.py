from datetime import datetime

from app import db


class Facility(db.Model):
    """A hospital, clinic, pharmacy, or NGO that can donate or request medical supplies."""

    __tablename__ = "facilities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    facility_type = db.Column(db.String(50), nullable=False)  # hospital, clinic, ngo, pharmacy
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    contact_email = db.Column(db.String(150), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    donations = db.relationship("SupplyDonation", backref="facility", lazy=True)
    requests = db.relationship("SupplyRequest", backref="facility", lazy=True)

    def __repr__(self):
        return f"<Facility {self.name} ({self.city}, {self.country})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "facility_type": self.facility_type,
            "city": self.city,
            "country": self.country,
            "verified": self.verified,
        }
