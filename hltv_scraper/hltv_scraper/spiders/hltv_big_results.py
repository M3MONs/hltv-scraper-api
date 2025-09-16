from typing import Any, Generator
import scrapy
from .parsers import ParsersFactory as PF


class HltvBigResultsSpider(scrapy.Spider):
    name = "hltv_big_results"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results"]

    def parse(self, response) -> Generator[Any, Any, None]:
        sublists = response.css("div.big-results")
        
        results = PF.get_parser("results").parse(sublists) or []
        yield from results
