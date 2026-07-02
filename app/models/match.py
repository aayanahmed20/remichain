from datetime import datetime

from app import db


class Match(db.Model):
    """A proposed or confirmed pairing between a donation and a request."""

    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    donation_id = db.Column(db.Integer, db.ForeignKey("supply_donations.id"), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey("supply_requests.id"), nullable=False)

    score = db.Column(db.Float, nullable=False)
    matched_quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="proposed")  # proposed, accepted, completed, rejected

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    donation = db.relationship("SupplyDonation", backref="matches")
    request = db.relationship("SupplyRequest", backref="matches")

    def to_dict(self):
        return {
            "id": self.id,
            "donation_id": self.donation_id,
            "request_id": self.request_id,
            "score": round(self.score, 2),
            "matched_quantity": self.matched_quantity,
            "status": self.status,
        }
