import cloudscraper
from flask import Request
import scrapy
from scrapy.http.response.html import HtmlResponse
from typing import Any, Generator
from .parsers import ParsersFactory as PF


class HltvPlayerStatsOverviewSpider(scrapy.Spider):
    name = "hltv_player_stats_overview"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, profile: str, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/stats/players/{profile}"]
        super().__init__(**kwargs)

    def start_requests(self) -> Generator[dict[str, None] | Request, Any, None]:
        scraper = cloudscraper.create_scraper()
        for url in self.start_urls:
            try:
                response_data = scraper.get(url)
                response = HtmlResponse(
                    url=url,
                    body=response_data.content,
                    encoding='utf-8'
                )
                yield from self.parse(response)
            except Exception as e:
                self.logger.error(f"Error fetching {url}: {e}")
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                )

    def parse(self, response):
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
