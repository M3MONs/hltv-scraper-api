import scrapy
from typing import Any
from .parsers import ParsersFactory as PF


class HltvPlayerStatsOverviewSpider(scrapy.Spider):
    name = "hltv_player_stats_overview"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, profile: str, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/stats/players/{profile}"]
        super().__init__(**kwargs)

    def parse(self, response):
        summary_parser = PF.get_parser('player_summary_stats')
        summary = summary_parser.parse(response.css("div.player-summary-stat-box"))
        
        role_stats_parser = PF.get_parser('player_role_stats')
        role_stats = role_stats_parser.parse(response.css("div.role-stats-container"))
        
        player_statistics_parser = PF.get_parser('player_statistics')
        player_statistics = player_statistics_parser.parse(response.css("div.statistics"))
        
        player_featured_rating_parser = PF.get_parser('player_featured_rating')
        featured_rating = player_featured_rating_parser.parse(response.css("div.featured-ratings-container"))

        yield {
            "summary": summary,
            "role_stats": role_stats,
            "player_statistics": player_statistics,
            "featured_rating": featured_rating
        }
