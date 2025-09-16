from typing import Any
from .parser import Parser

class TeamProfileLinkParser(Parser):
    @staticmethod
    def parse(response) -> list[dict[str, Any]]:
        teams = response.css("div.search a[href^='/team/']")
        return [
            {
                "name": team.css("a::text").get(),
                "img": team.css("a img::attr(src)").get(),
                "link": team.css("a::attr(href)").get(),
            }
            for team in teams
        ]