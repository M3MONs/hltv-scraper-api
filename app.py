import datetime
import os
from flask import Flask, jsonify
from flask_limiter import Limiter

from classes.spider_manager import SpiderManager

app = Flask(__name__)
app.json.sort_keys = False

limiter = Limiter(app, default_limits=["1 per second"])

BASE_DIR = "./hltv_scraper"
SM = SpiderManager(BASE_DIR)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)


@app.route("/results/", defaults={"offset": 0})
@app.route("/results/<offset>/", methods=["GET"])
def results(offset: int):
    name = "hltv_results"
    path = f"results/results_{offset}"
    args = f"-a offset={offset} -o {DATA_DIR}/{path}.json"
    
    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


@app.route("/results/big", methods=["GET"])
def big_results():
    name = "hltv_big_results"
    path = "big_results"
    args = f"-o {DATA_DIR}/{path}.json"
    
    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


@app.route("/top_teams/", methods=["GET"])
def top30():
    name = "hltv_top30"
    path = "top_teams"
    args = f"-o {DATA_DIR}/{path}.json"

    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


@app.route("/upcoming_matches/", methods=["GET"])
def upcoming_matches():
    name = "hltv_upcoming_matches"
    path = "upcoming_matches"
    args = f"-o {DATA_DIR}/{path}.json"

    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


today = datetime.date.today()


@app.route("/news/", defaults={"year": today.year, "month": today.strftime("%B")})
@app.route("/news/<year>/<month>/")
@limiter.limit("1 per second")
def news(year: str, month: str):
    name = "hltv_news"
    path = f"news/news_{year}_{month}"
    args = f"-a year={year} -a month={month} -o {DATA_DIR}/{path}.json"
    
    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


@app.route("/team/<name>/", methods=["GET"])
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


@app.route("/team/matches/<id>/", defaults={"offset": 0})
@app.route("/team/matches/<id>/<offset>/", methods=["GET"])
@limiter.limit("1 per second")
def team_matches(id: str, offset: int):
    name = "hltv_team_matches"
    path = f"team_matches/{id}_{offset}"
    args = f"-a id={id} -a offset={offset} -o {DATA_DIR}/{path}.json"
    
    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


@app.route("/profile/team/<id>/<team>/", methods=["GET"])
@limiter.limit("1 per second")
def team_profile(id: str, team: str):
    name = "hltv_team"
    path = f"team/{team}"
    args = f"-a team=/team/{id}/{team} -o {DATA_DIR}/{path}.json"
    
    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


@app.route("/player/<name>/", methods=["GET"])
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


@app.route("/profile/player/<id>/<player>/", methods=["GET"])
@limiter.limit("1 per second")
def player_profile(id: str, player: str):
    name = "hltv_player"
    path = f"player/{player}"
    args = f"-a profile=/player/{id}/{player} -o {DATA_DIR}/{path}.json"
    
    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))

@app.route("/match/<id>/<match>/", methods=["GET"])
def match(id: str, match: str):
    name = "hltv_match"
    match_link = f"{id}/{match}"
    path = f"match/{id}_{match}"
    args = f"-a match={match_link} -o {DATA_DIR}/{path}.json"
    
    SM.execute(name, path, args)
    return jsonify(SM.get_result(path))


if __name__ == "__main__":
    app.run(debug=True, port=8000)
