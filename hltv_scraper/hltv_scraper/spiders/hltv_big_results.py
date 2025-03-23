import scrapy
from .parsers import ParsersFactory as PF


class HltvBigResultsSpider(scrapy.Spider):
    name = "hltv_big_results"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results?offset=0"]

    def parse(self, response):
        results = response.css("div.big-results .result-con")

        for result in results:
            data = PF.get_parser("match").parse(result)

            yield data
