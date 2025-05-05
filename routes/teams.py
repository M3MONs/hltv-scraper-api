from flask import Blueprint, jsonify, current_app

from config import API_PREFIX, DATA_DIR
from services.utils import execute_spider

teams_bp = Blueprint("teams", __name__, url_prefix=f"{API_PREFIX}/teams")

@teams_bp.route("/rankings", defaults={"type": "hltv", "year": "", "month": "", "day": 0})
@teams_bp.route("/rankings/<string:type>", defaults={"year": "", "month": "", "day": 0})
@teams_bp.route("/rankings/<string:type>/<string:year>/<string:month>/<int:day>", methods=["GET"])
def top30(type: str, year: str = "", month: str = "", day: int = 0):
    """Get team rankings from HLTV or VALVE RANKING."""
    name = "hltv_valve_ranking" if type == "valve" else "hltv_top30"
    path = f"rankings/{type}" if year == "" and month == "" and day == 0 else f"rankings/{type}_{year}_{month}_{day}"
    args = f"-a year={year} -a month={month} -a day={day} -o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)

@teams_bp.route("/search/<string:name>", methods=["GET"])
def search_team(name: str):
    """Search team profiles by name from HLTV."""
    sm = current_app.spider_manager
    name = name.lower()

    if not sm.is_profile("teams_profile", name):
        sm.run_spider("hltv_teams_search", name, f"-a team={name}")

    if not sm.is_profile("teams_profile", name):
        return jsonify({"error": "Team not found!"}), 404

    profiles = sm.get_profile("teams_profile", name)
    return jsonify(profiles)

@teams_bp.route("/<string:id>/matches", defaults={"offset": 0})
@teams_bp.route("/<string:id>/matches/<int:offset>", methods=["GET"])
def team_matches(id: str, offset: int):
    """Get team matches from HLTV."""
    name = "hltv_team_matches"
    path = f"team_matches/{id}_{offset}"
    args = f"-a id={id} -a offset={offset} -o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)

@teams_bp.route("/<string:id>/<string:team_name>", methods=["GET"])
def team_profile(id: str, team_name: str):
    """Get team profile from HLTV."""
    name = "hltv_team"
    path = f"team/{team_name}"
    args = f"-a team=/team/{id}/{team_name} -o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)