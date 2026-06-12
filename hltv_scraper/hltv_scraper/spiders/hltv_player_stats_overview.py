import json
from pathlib import Path
from typing import Any

import scrapy

from .parsers import ParsersFactory as PF

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SESSION_FILE = PROJECT_ROOT / "cf_session.json"


class HltvPlayerStatsOverviewSpider(scrapy.Spider):
    name = "hltv_player_stats_overview"
    allowed_domains = ["www.hltv.org"]

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 3,  # keep request rate low to avoid triggering a new challenge
        "CONCURRENT_REQUESTS": 1,
    }

    def __init__(self, profile: str, session_file: str | None = None, **kwargs: Any):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.hltv.org/stats/players/{profile}"]

        session_path = Path(session_file) if session_file else DEFAULT_SESSION_FILE
        if not session_path.exists():
            raise FileNotFoundError(
                f"Session file not found: {session_path}. "
                f"Run grab_cf.py first to obtain cf_clearance, "
                f"or pass the path explicitly: -a session_file=/path/to/cf_session.json"
            )

        session = json.loads(session_path.read_text())
        self.cf_clearance = session["cf_clearance"]
        self.user_agent = session["user_agent"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                cookies={"cf_clearance": self.cf_clearance},
                headers={
                    "User-Agent": self.user_agent,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                },
                meta={"impersonate": "chrome131"},
                callback=self.parse,
                errback=self.on_error,
            )

    def on_error(self, failure):
        self.logger.error(
            f"Request failed: {failure}. "
            f"If status is 403 — cf_clearance expired or IP/UA mismatch. Re-run grab_cf.py."
        )

    def parse(self, response):
        if response.status == 403 or "challenge" in response.text[:2000].lower():
            self.logger.error("Received a challenge page despite the cookie — refresh cf_clearance by re-running grab_cf.py.")
            return

        summary_parser = PF.get_parser('player_summary_stats')
        summary = summary_parser.parse(response.css("div.player-summary-stat-box"))

        role_stats_parser = PF.get_parser('player_role_stats')
        role_stats = role_stats_parser.parse(response.css("div.role-stats-container"))

        player_statistics_parser = PF.get_parser('player_statistics')
        player_statistics = player_statistics_parser.parse(response.css("div.statistics"))

        yield {
            "summary": summary,
            "role_stats": role_stats,
            "player_statistics": player_statistics,
        }