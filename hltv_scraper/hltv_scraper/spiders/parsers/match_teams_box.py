from typing import Any
from .parser import Parser
from .match_team import MatchTeamParser as MTP

class MatchTeamsBoxParser(Parser):
    @staticmethod
    def parse(teams_box) -> dict[str, Any]:
        return {
        "date": teams_box.css("div.date::text").get(),
        "hour": teams_box.css("div.time::text").get(),
        "event": teams_box.css("div.event ::text").get(),
        "team1": MTP.parse(teams_box, 1),
        "team2": MTP.parse(teams_box, 2),
    }