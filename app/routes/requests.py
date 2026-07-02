from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db
from app.models import SupplyRequest, Facility
from app.services.matching import find_matches_for_request, create_match

requests_bp = Blueprint("requests", __name__)


@requests_bp.route("/request", methods=["GET", "POST"])
def request_supply():
    if request.method == "POST":
        need = SupplyRequest(
            facility_id=int(request.form["facility_id"]),
            item_name=request.form["item_name"].strip(),
            category=request.form["category"],
            quantity_needed=int(request.form["quantity_needed"]),
            unit=request.form.get("unit", "units"),
            urgency=request.form.get("urgency", "medium"),
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(need)
        db.session.commit()

        # Immediately try to propose a match so the requester sees value right away
        best = find_matches_for_request(need, limit=1)
        if best:
            donation, score = best[0]
            create_match(donation, need, score)
            flash(f"Request posted — a possible match was found for {need.item_name}!", "success")
        else:
            flash(f"Request posted for {need.item_name}. We'll match it as donations come in.", "info")

        return redirect(url_for("main.dashboard"))

    facilities = Facility.query.order_by(Facility.name).all()
    return render_template("request.html", facilities=facilities)
