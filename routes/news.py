from flask import Blueprint

from config import API_PREFIX, DATA_DIR, TODAY
from services.utils import execute_spider

news_bp = Blueprint("news", __name__, url_prefix=f"{API_PREFIX}/news")

@news_bp.route("", defaults={"year": TODAY.year, "month": TODAY.strftime("%B")})
@news_bp.route("<int:year>/<string:month>/")
def news(year: str, month: str):
    """Get news from HLTV."""
    name = "hltv_news"
    path = f"news/news_{year}_{month}"
    args = f"-a year={year} -a month={month} -o {DATA_DIR}/{path}.json"

    return execute_spider(name, path, args)