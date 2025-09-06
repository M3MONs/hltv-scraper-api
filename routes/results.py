from flask import Blueprint, jsonify

from hltv_scraper import HLTVScraper

results_bp = Blueprint("results", __name__, url_prefix="/api/v1/results")

@results_bp.route("/", defaults={"offset": 0})
@results_bp.route("/<int:offset>", methods=["GET"])
def results(offset: int):
    """Get results from HLTV."""
    try:
        data = HLTVScraper.get_results(offset)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@results_bp.route("/featured", methods=["GET"])
def big_results():
    """Get featured results from HLTV."""
    try:
        data = HLTVScraper.get_big_results()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500