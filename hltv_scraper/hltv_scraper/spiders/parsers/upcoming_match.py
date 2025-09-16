from typing import Any
from .parser import Parser
from .upcoming_match_team import UpcomingMatchTeamParser as UMTP
from ..utils import is_team_in_upcoming_match

class UpcomingMatchParser(Parser):
    @staticmethod
    def parse(match, date: str = "") -> dict[str, Any] | None:
        if is_team_in_upcoming_match(match):
            return {
                "hour": match.css("div.match-time::text").get(),
                "date": date,
                "link": match.css("a.match-info::attr(href)").get(),
                "meta": match.css("div.match-meta::text").get(),
                "event": match.css("div.match-event::attr(data-event-headline)").get(),
                "team1": UMTP.parse(match, 1),
                "team2": UMTP.parse(match, 2),
            }