import os
from flask import Flask, jsonify
from flask_limiter import Limiter

from classes.spider_manager import SpiderManager
from config import API_PREFIX, BASE_DIR, DATA_DIR, DEFAULT_RATE_LIMIT, TODAY

app = Flask(__name__)
app.json.sort_keys = False

limiter = Limiter(app, default_limits=[DEFAULT_RATE_LIMIT])

SM = SpiderManager(BASE_DIR)
os.makedirs(DATA_DIR, exist_ok=True)

@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = jsonify({"error": str(e)})
    response.status_code = 500
    return response

@app.route(f"{API_PREFIX}/results", defaults={"offset": 0})
@app.route(f"{API_PREFIX}/results/<int:offset>", methods=["GET"])
def results(offset: int):
    """Get results from HLTV."""
    name = "hltv_results"
    path = f"results/results_{offset}"
    args = f"-a offset={offset} -o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)


@app.route(f"{API_PREFIX}/results/featured/", methods=["GET"])
def big_results():
    """Get featured results from HLTV."""
    name = "hltv_big_results"
    path = "big_results"
    args = f"-o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)

@app.route(f"{API_PREFIX}/teams/rankings", defaults={"type": "hltv", "year": "", "month": "", "day": 0})
@app.route(f"{API_PREFIX}/teams/rankings/<string:type>", defaults={"year": "", "month": "", "day": 0})
@app.route(f"{API_PREFIX}/teams/rankings/<string:type>/<string:year>/<string:month>/<int:day>", methods=["GET"])
def top30(type: str, year: str = "", month: str = "", day: int = 0):
    """Get team rankings from HLTV or VALVE RANKING."""
    name = "hltv_valve_ranking" if type == "valve" else "hltv_top30"
    path = f"rankings/{type}" if year == "" and month == "" and day == 0 else f"rankings/{type}_{year}_{month}_{day}"
    args = f"-a year={year} -a month={month} -a day={day} -o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)


@app.route(f"{API_PREFIX}/matches/upcoming", methods=["GET"])
def upcoming_matches():
    """Get upcoming matches from HLTV."""
    name = "hltv_upcoming_matches"
    path = "upcoming_matches"
    args = f"-o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)


@app.route(f"{API_PREFIX}/news", defaults={"year": TODAY.year, "month": TODAY.strftime("%B")})
@app.route(f"{API_PREFIX}/news/<int:year>/<string:month>/")
@limiter.limit("1 per second")
def news(year: str, month: str):
    """Get news from HLTV."""
    name = "hltv_news"
    path = f"news/news_{year}_{month}"
    args = f"-a year={year} -a month={month} -o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)


@app.route(f"{API_PREFIX}/teams/search/<string:name>", methods=["GET"])
@limiter.limit("1 per second")
def team(name: str):
    """Search team profiles by name from HLTV."""
    spider_name = "hltv_teams_search"
    name = name.lower()

    if not SM.is_profile("teams_profile", name):
        SM.run_spider(spider_name, name, f"-a team={name}")

    if not SM.is_profile("teams_profile", name):
        return "Team not found!"

    profiles = SM.get_profile("teams_profile", name)

    return jsonify(profiles)


@app.route(f"{API_PREFIX}/teams/<string:id>/matches", defaults={"offset": 0})
@app.route(f"{API_PREFIX}/teams/<string:id>/matches/<int:offset>", methods=["GET"])
@limiter.limit("1 per second")
def team_matches(id: str, offset: int):
    """Get team matches from HLTV."""
    name = "hltv_team_matches"
    path = f"team_matches/{id}_{offset}"
    args = f"-a id={id} -a offset={offset} -o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)


@app.route(f"{API_PREFIX}/teams/<string:id>/<string:team_name>", methods=["GET"])
@limiter.limit("1 per second")
def team_profile(id: str, team_name: str):
    """Get team profile from HLTV."""
    name = "hltv_team"
    path = f"team/{team_name}"
    args = f"-a team=/team/{id}/{team_name} -o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)


@app.route(f"{API_PREFIX}/players/search/<string:name>", methods=["GET"])
@limiter.limit("1 per second")
def player(name: str):
    """Search player profiles by name from HLTV."""
    name = name.lower()
    spider_name = "hltv_players_search"

    if not SM.is_profile("players_profiles", name):
        SM.run_spider(spider_name, name, f"-a player={name}")

    if not SM.is_profile("players_profiles", name):
        return "Player not found!"

    profiles = SM.get_profile("players_profiles", name)

    return jsonify(profiles)


@app.route(f"{API_PREFIX}/players/<string:id>/<string:player_name>", methods=["GET"])
@limiter.limit("1 per second")
def player_profile(id: str, player_name: str):
    """Get player profile from HLTV."""
    name = "hltv_player"
    path = f"player/{player_name}"
    args = f"-a profile=/player/{id}/{player_name} -o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)


@app.route(f"{API_PREFIX}/matches/<string:id>/<string:match_name>", methods=["GET"])
def match(id: str, match_name: str):
    """Get match details from HLTV."""
    name = "hltv_match"
    match_link = f"{id}/{match_name}"
    path = f"match/{id}_{match_name}"
    args = f"-a match={match_link} -o {DATA_DIR}/{path}.json"


    return execute_spider(name, path, args)


def execute_spider(name: str, path: str, args: str) -> None:
    """Execute the spider with the given name and arguments."""
    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
