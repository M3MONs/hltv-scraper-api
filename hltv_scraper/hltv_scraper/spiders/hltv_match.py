from flask import Request
import scrapy
from typing import Any, Generator
import cloudscraper
from scrapy.http.response.html import HtmlResponse
from .parsers import ParsersFactory as PF


class HltvMatchSpider(scrapy.Spider):
    name = "hltv_match"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, match: str, **kwargs: Any) -> None:
        self.start_urls = [f"https://www.hltv.org/matches/{match}"]
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

    def parse(self, response) -> Generator[dict[str, None], Any, None]:
        teams_box = PF.get_parser("match_teams_box").parse(response.css(".teamsBox"))
        maps_score = PF.get_parser("map_holders").parse(response)
        player_stats = PF.get_parser("table_stats").parse(response.css("#all-content"))

        yield {"match": teams_box, "maps": maps_score, "stats": player_stats}
