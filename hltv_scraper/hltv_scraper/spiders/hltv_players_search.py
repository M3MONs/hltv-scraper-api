from typing import Any
import scrapy
from .parsers import ParsersFactory as PF
from .utils import update_json_data


class HltvPlayersSearchSpider(scrapy.Spider):
    name = "hltv_players_search"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, player: str | None = None, **kwargs: Any) -> None:
        self.start_urls = [f"https://www.hltv.org/search?query={player}"]
        self.player_search = player
        super().__init__(**kwargs)

    def parse(self, response) -> None:
        profiles = PF.get_parser("player_profile_link").parse(response, self.player_search)

        if not profiles:
            return

        extracted_profiles = PF.get_parser("players_profile").parse(profiles)

        if extracted_profiles:
            data = {f"{self.player_search}": extracted_profiles}
            update_json_data("players_profiles", data)
