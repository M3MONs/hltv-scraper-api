from typing import Literal
from flask import Blueprint, Response, jsonify
from flasgger import swag_from

from hltv_scraper import HLTVScraper

players_bp = Blueprint("players", __name__, url_prefix="/api/v1/players")

@players_bp.route("/search/<string:name>", methods=["GET"])
@swag_from('../swagger_specs/players_search.yml')
def player(name: str) -> Response | tuple[Response, Literal[404]] | tuple[Response, Literal[500]]:
    """Search player profiles by name from HLTV."""
    try:
        data = HLTVScraper.search_player(name)
        return jsonify(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@players_bp.route("/<string:id>/<string:player_name>", methods=["GET"])
@swag_from('../swagger_specs/players_profile.yml')
def player_profile(id: str, player_name: str) -> Response | tuple[Response, Literal[500]]:
    """Get player profile from HLTV."""
    try:
        data = HLTVScraper.get_player_profile(id, player_name)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@players_bp.route("/stats/overview/<string:id>/<string:player_name>", methods=["GET"])
@swag_from('../swagger_specs/players_stats_overview.yml')
def player_stats_overview(id: str, player_name: str) -> Response | tuple[Response, Literal[500]]:
    """Get player statistics overview from HLTV."""
    try:
        data = HLTVScraper.get_player_stats_overview(id, player_name)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500