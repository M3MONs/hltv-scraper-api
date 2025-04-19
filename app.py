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


@app.route(f"{API_PREFIX}/results", defaults={"offset": 0})
@app.route(f"{API_PREFIX}/results/<int:offset>", methods=["GET"])
def results(offset: int):
    name = "hltv_results"
    path = f"results/results_{offset}"
    args = f"-a offset={offset} -o {DATA_DIR}/{path}.json"

    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


# TODO: Check if this route is needed
# @app.route("/results/big/", methods=["GET"])
# def big_results():
#     name = "hltv_big_results"
#     path = "big_results"
#     args = f"-o {DATA_DIR}/{path}.json"

#     SM.execute(name, path, args)
#     return jsonify(SM.get_result(path))


@app.route(f"{API_PREFIX}/teams/rankings", methods=["GET"])
def top30():
    name = "hltv_top30"
    path = "top_teams"
    args = f"-o {DATA_DIR}/{path}.json"

    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


@app.route(f"{API_PREFIX}/matches/upcoming", methods=["GET"])
def upcoming_matches():
    name = "hltv_upcoming_matches"
    path = "upcoming_matches"
    args = f"-o {DATA_DIR}/{path}.json"

    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


@app.route(f"{API_PREFIX}/news", defaults={"year": TODAY.year, "month": TODAY.strftime("%B")})
@app.route(f"{API_PREFIX}/news/<int:year>/<string:month>/")
@limiter.limit("1 per second")
def news(year: str, month: str):
    name = "hltv_news"
    path = f"news/news_{year}_{month}"
    args = f"-a year={year} -a month={month} -o {DATA_DIR}/{path}.json"

    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


@app.route(f"{API_PREFIX}/teams/search/<string:name>", methods=["GET"])
@limiter.limit("1 per second")
def team(name: str):
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
    name = "hltv_team_matches"
    path = f"team_matches/{id}_{offset}"
    args = f"-a id={id} -a offset={offset} -o {DATA_DIR}/{path}.json"

    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


@app.route(f"{API_PREFIX}/teams/<string:id>/<string:team_name>", methods=["GET"])
@limiter.limit("1 per second")
def team_profile(id: str, team_name: str):
    name = "hltv_team"
    path = f"team/{team_name}"
    args = f"-a team=/team/{id}/{team_name} -o {DATA_DIR}/{path}.json"

    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


@app.route(f"{API_PREFIX}/players/search/<string:name>", methods=["GET"])
@limiter.limit("1 per second")
def player(name: str):
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
    name = "hltv_player"
    path = f"player/{player_name}"
    args = f"-a profile=/player/{id}/{player_name} -o {DATA_DIR}/{path}.json"

    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


@app.route(f"{API_PREFIX}/matches/<string:id>/<string:match_name>", methods=["GET"])
def match(id: str, match_name: str):
    name = "hltv_match"
    match_link = f"{id}/{match_name}"
    path = f"match/{id}_{match_name}"
    args = f"-a match={match_link} -o {DATA_DIR}/{path}.json"

    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


if __name__ == "__main__":
    app.run(debug=True, port=8000)
