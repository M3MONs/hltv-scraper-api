from flask import Blueprint

from config import API_PREFIX, DATA_DIR
from services.utils import execute_spider

matches_bp = Blueprint("matches", __name__, url_prefix=f"{API_PREFIX}/matches")

@matches_bp.route("/upcoming", methods=["GET"])
def upcoming_matches():
    """Get upcoming matches from HLTV."""
    name = "hltv_upcoming_matches"
    path = "upcoming_matches"
    args = f"-o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)

@matches_bp.route("/<string:id>/<string:match_name>", methods=["GET"])
def match(id: str, match_name: str):
    """Get match details from HLTV."""
    name = "hltv_match"
    match_link = f"{id}/{match_name}"
    path = f"match/{id}_{match_name}"
    args = f"-a match={match_link} -o {DATA_DIR}/{path}.json"


    return execute_spider(name, path, args)