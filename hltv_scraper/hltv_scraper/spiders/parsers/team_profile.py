from typing import Any
from .parser import Parser
from .team_squad import TeamSquadParser as TSP
from .team_matches import TeamMatchesParser as TMP

class TeamProfileParser(Parser):
    @staticmethod
    def parse(response) -> dict[str, Any] | None:
        team_data = {
        "name": response.css(".profile-team-name::text").get(),
        "ranking": response.css("span.right a::text").get(),
        "logo": response.css("img.teamlogo::attr(src)").get(),
        "country": response.css("div.team-country::text").get(),
        "country_img": f'https://www.hltv.org{response.css("div.team-country img::attr(src)").get()}',
        "squad": TSP.parse(response),
        "matches": TMP.parse(response),
        }
        if team_data["name"]:
            return team_data