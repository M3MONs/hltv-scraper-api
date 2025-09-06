from flask import Blueprint, jsonify

from hltv_scraper import HLTVScraper

teams_bp = Blueprint("teams", __name__, url_prefix="/api/v1/teams")

@teams_bp.route("/rankings", defaults={"type": "hltv", "year": "", "month": "", "day": 0})
@teams_bp.route("/rankings/<string:type>", defaults={"year": "", "month": "", "day": 0})
@teams_bp.route("/rankings/<string:type>/<string:year>/<string:month>/<int:day>", methods=["GET"])
def top30(type: str, year: str = "", month: str = "", day: int = 0):
    """Get team rankings from HLTV or VALVE RANKING."""
    try:
        data = HLTVScraper.get_team_rankings(type, year, month, day)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@teams_bp.route("/search/<string:name>", methods=["GET"])
def search_team(name: str):
    """Search team profiles by name from HLTV."""
    try:
        data = HLTVScraper.search_team(name)
        return jsonify(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@teams_bp.route("/<string:id>/matches", defaults={"offset": 0})
@teams_bp.route("/<string:id>/matches/<int:offset>", methods=["GET"])
def team_matches(id: str, offset: int):
    """Get team matches from HLTV."""
    try:
        data = HLTVScraper.get_team_matches(id, offset)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@teams_bp.route("/<string:id>/<string:team_name>", methods=["GET"])
def team_profile(id: str, team_name: str):
    """Get team profile from HLTV."""
    try:
        data = HLTVScraper.get_team_profile(id, team_name)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500