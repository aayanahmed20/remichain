from flask import Blueprint, jsonify

from app.models import SupplyDonation, SupplyRequest, Match
from app.services.matching import run_matching_pass, find_matches_for_request

api_bp = Blueprint("api", __name__)


@api_bp.route("/donations", methods=["GET"])
def list_donations():
    return jsonify([d.to_dict() for d in SupplyDonation.query.all()])


@api_bp.route("/requests", methods=["GET"])
def list_requests():
    return jsonify([r.to_dict() for r in SupplyRequest.query.all()])


@api_bp.route("/matches", methods=["GET"])
def list_matches():
    return jsonify([m.to_dict() for m in Match.query.all()])


@api_bp.route("/requests/<int:request_id>/candidates", methods=["GET"])
def candidates_for_request(request_id):
    req = SupplyRequest.query.get_or_404(request_id)
    matches = find_matches_for_request(req, limit=5)
    return jsonify([
        {"donation": d.to_dict(), "score": round(score, 2)} for d, score in matches
    ])


@api_bp.route("/run-matching", methods=["POST"])
def trigger_matching_pass():
    created = run_matching_pass()
    return jsonify({"matches_created": len(created), "matches": [m.to_dict() for m in created]})
