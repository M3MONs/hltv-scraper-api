import scrapy
from typing import Any
from .parsers import ParsersFactory as PF
from .utils import update_json_data


class HltvTeamsSearchSpider(scrapy.Spider):
    name = "hltv_teams_search"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, team: str, **kwargs: Any) -> None:
        self.start_urls = [f"https://www.hltv.org/search?query={team}"]
        self.team_name = team
        super().__init__(**kwargs)

    def parse(self, response) -> None:
        profile_link = PF.get_parser("teams_profile_link").parse(response)
        if profile_link:
            data = {f"{self.team_name}": profile_link}
            update_json_data("teams_profile", data)
