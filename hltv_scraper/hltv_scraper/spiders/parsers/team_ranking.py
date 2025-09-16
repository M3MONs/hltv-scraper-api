from typing import Any
from .parser import Parser


class TeamRankingParser(Parser):
    @staticmethod
    def parse(team) -> dict[str, Any]:
        return {
            "position": team.css("span.position::text").get(),
            "name": team.css(".name::text").get(),
            "id": team.css(".lineup-con .more a.moreLink::attr(href)").re_first(r"/team/(\d+)"),
            "link": team.css(".lineup-con .more a.moreLink::attr(href)").get(),
            "logo": team.css("span.team-logo img::attr(src)").get(),
            "points": team.css("span.points::text").get()[1:],
            "players": team.css("div.playersLine .rankingNicknames span::text").getall(),
        }
