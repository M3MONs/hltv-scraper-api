from flask import Blueprint

from config import API_PREFIX, DATA_DIR
from services.utils import execute_spider

results_bp = Blueprint("results", __name__, url_prefix=f"{API_PREFIX}/results")

@results_bp.route("/", defaults={"offset": 0})
@results_bp.route("/<int:offset>", methods=["GET"])
def results(offset: int):
    """Get results from HLTV."""
    name = "hltv_results"
    path = f"results/results_{offset}"
    args = f"-a offset={offset} -o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)

@results_bp.route("/featured", methods=["GET"])
def big_results():
    """Get featured results from HLTV."""
    name = "hltv_big_results"
    path = "big_results"
    args = f"-o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)