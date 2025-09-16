import scrapy
from typing import Any, Generator
from .parsers import ParsersFactory as PF


class HltvPlayerSpider(scrapy.Spider):
    name = "hltv_player"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, profile: str, **kwargs: Any) -> None:
        self.start_urls = [f"https://www.hltv.org{profile}"]
        super().__init__(**kwargs)

    def parse(self, response) -> Generator[None, Any, None]:
        profile = response.css("div.playerProfile")
        data = PF.get_parser('player_profile').parse(profile)
        yield data
