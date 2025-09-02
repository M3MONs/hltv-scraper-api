from flask import Blueprint, jsonify, current_app
from typing import Any, cast

from config import API_PREFIX, DATA_DIR
from services.utils import execute_spider

players_bp = Blueprint("players", __name__, url_prefix=f"{API_PREFIX}/players")
@players_bp.route("/search/<string:name>", methods=["GET"])
def player(name: str):
    """Search player profiles by name from HLTV."""
    sm = cast(Any, current_app).spider_manager
    name = name.lower()
    spider_name = "hltv_players_search"

    if not sm.is_profile("players_profiles", name):
        sm.run_spider(spider_name, name, f"-a player={name}")

    if not sm.is_profile("players_profiles", name):
        return "Player not found!"

    profiles = sm.get_profile("players_profiles", name)

    return jsonify(profiles)


@players_bp.route("<string:id>/<string:player_name>", methods=["GET"])
def player_profile(id: str, player_name: str):
    """Get player profile from HLTV."""
    name = "hltv_player"
    path = f"player/{player_name}"
    args = f"-a profile=/player/{id}/{player_name} -o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)