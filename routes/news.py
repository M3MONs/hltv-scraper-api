from flask import Blueprint, Response, jsonify
from typing import Literal, Optional
from flasgger import swag_from

from hltv_scraper import HLTVScraper

news_bp = Blueprint("news", __name__, url_prefix="/api/v1/news")

@news_bp.route("", defaults={"year": None, "month": None})
@news_bp.route("/<int:year>/<string:month>/")
@swag_from('../swagger_specs/news_list.yml')
def news(year: Optional[int] = None, month: Optional[str] = None) -> Response | tuple[Response, Literal[500]]:
    """Get news from HLTV."""
    if year is None or month is None:
        from datetime import datetime
        now = datetime.now()
        year = now.year
        month = now.strftime("%B")
    try:
        data = HLTVScraper.get_news(year, month)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500