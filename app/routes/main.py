from flask import Blueprint, render_template

from app.models import SupplyDonation, SupplyRequest, Match, Facility

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    stats = {
        "facilities": Facility.query.count(),
        "available_donations": SupplyDonation.query.filter_by(status="available").count(),
        "open_requests": SupplyRequest.query.filter(
            SupplyRequest.status.in_(["open", "partially_fulfilled"])
        ).count(),
        "matches_made": Match.query.count(),
    }
    return render_template("index.html", stats=stats)


@main_bp.route("/dashboard")
def dashboard():
    donations = SupplyDonation.query.order_by(SupplyDonation.created_at.desc()).limit(20).all()
    requests_ = SupplyRequest.query.order_by(SupplyRequest.created_at.desc()).limit(20).all()
    matches = Match.query.order_by(Match.created_at.desc()).limit(20).all()
    return render_template(
        "dashboard.html", donations=donations, requests=requests_, matches=matches
    )
