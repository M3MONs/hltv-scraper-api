from flask import Blueprint, jsonify

from hltv_scraper import HLTVScraper

matches_bp = Blueprint("matches", __name__, url_prefix="/api/v1/matches")

@matches_bp.route("/upcoming", methods=["GET"])
def upcoming_matches():
    """Get upcoming matches from HLTV."""
    try:
        data = HLTVScraper.get_upcoming_matches()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@matches_bp.route("/<string:id>/<string:match_name>", methods=["GET"])
def match(id: str, match_name: str):
    """Get match details from HLTV."""
    try:
        data = HLTVScraper.get_match(id, match_name)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500