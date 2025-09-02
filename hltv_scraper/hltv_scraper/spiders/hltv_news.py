import scrapy
from typing import Any
from .parsers import ParsersFactory as PF


class HltvNewsSpider(scrapy.Spider):
    name = "hltv_news"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, year: str, month: str, **kwargs: Any):
        self.date = f"{year}/{month}"
        self.start_urls = [f"https://www.hltv.org/news/archive/{self.date}"]
        super().__init__(**kwargs)

    def parse(self, response):
        articles = response.css(".article")
        data = PF.get_parser("news").parse(articles)
        yield from data or []
