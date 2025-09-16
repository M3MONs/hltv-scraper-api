from typing import Any, Generator
import scrapy
from .parsers import ParsersFactory as PF
from scrapy_selenium import SeleniumRequest


class HltvUpcomingMatchesSpider(scrapy.Spider):
    name = "hltv_upcoming_matches"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/matches"]

    def start_requests(self) -> Generator[SeleniumRequest, Any, None]:
        yield SeleniumRequest(
            url = self.start_urls[0],
            callback = self.parse,
            wait_time = 5,
            script="localStorage.setItem('matches-sortBy', 'time');",
            headers={
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.hltv.org/',
            'Connection': 'keep-alive',
            },
        )

    def parse(self, response) -> Generator[Any, Any, None]:
        matches_sections = response.css("div.matches-list-section")
        
        upcoming_matches = PF.get_parser("upcoming_matches").parse(matches_sections) or []
        yield from upcoming_matches
