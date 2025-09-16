from typing import Any
from .parser import Parser
from .single_team import SingleTeamParser as STP


class TeamMatchesParser(Parser):
    @staticmethod
    def parse(response) -> list[dict[str, Any]]:
        matches = response.css("tr.team-row")
        return [
            {
                "match_link": match.css("td:nth-child(3) a::attr(href)").get(),
                "date": match.css(".date-cell span::text").get(),
                "team1": STP.parse(match, 1, 1),
                "team2": STP.parse(match, 2, 3),
            }
            for match in matches
        ]
