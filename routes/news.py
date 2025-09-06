from flask import Blueprint, jsonify
from typing import Optional

from hltv_scraper import HLTVScraper

news_bp = Blueprint("news", __name__, url_prefix="/api/v1/news")

@news_bp.route("", defaults={"year": None, "month": None})
@news_bp.route("<int:year>/<string:month>/")
def news(year: Optional[int] = None, month: Optional[str] = None):
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