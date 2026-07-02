from datetime import datetime

from app import db


class SupplyRequest(db.Model):
    """A request for medical supplies raised by a facility in need."""

    __tablename__ = "supply_requests"

    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey("facilities.id"), nullable=False)

    item_name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    quantity_needed = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(30), default="units")

    urgency = db.Column(db.String(20), default="medium")  # low, medium, high, critical
    status = db.Column(db.String(20), default="open")  # open, partially_fulfilled, fulfilled
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    URGENCY_SCORES = {"low": 1, "medium": 2, "high": 3, "critical": 4}

    @property
    def urgency_score(self):
        return self.URGENCY_SCORES.get(self.urgency, 2)

    def to_dict(self):
        return {
            "id": self.id,
            "facility_id": self.facility_id,
            "item_name": self.item_name,
            "category": self.category,
            "quantity_needed": self.quantity_needed,
            "unit": self.unit,
            "urgency": self.urgency,
            "status": self.status,
        }
