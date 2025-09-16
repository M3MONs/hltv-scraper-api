from typing import Any, Generator
import scrapy
from .parsers import ParsersFactory as PF


class HltvTeamMatchesSpider(scrapy.Spider):
    name = "hltv_team_matches"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, id: str, offset: int = 0, **kwargs: Any):
        self.start_urls = [f"https://www.hltv.org/results?offset={offset}&team={id}"]
        super().__init__(**kwargs)

    def parse(self, response) -> Generator[Any, Any, None]:
        results = response.css(".results-all .a-reset")
        data = PF.get_parser("team_results").parse(results) or []
        yield from data
