from typing import Any, Generator
import scrapy
from .parsers import ParsersFactory as PF


class HltvTeamSpider(scrapy.Spider):
    name = "hltv_team"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, team: str, **kwargs: Any) -> None:
        self.start_urls = [f"https://www.hltv.org{team}#tab-matchesBox"]
        super().__init__(**kwargs)

    def parse(self, response) -> Generator[None, Any, None]:
        yield PF.get_parser("team_profile").parse(response)
