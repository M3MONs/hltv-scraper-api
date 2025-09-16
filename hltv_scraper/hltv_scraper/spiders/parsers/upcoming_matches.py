from typing import Any
from .date import UpcomingMatchDateFormatter
from .parser import Parser
from .upcoming_match import UpcomingMatchParser as UMP

class UpcomingMatchesParser(Parser):
    @staticmethod
    def parse(matches_sublists) -> list[dict[str, Any]]:
        all_upcoming_matches = []

        for sublist in matches_sublists:
            date = sublist.css(".matches-list-headline::text").get()
            standard_date = ""

            if date:
                standard_date = UpcomingMatchDateFormatter.format(date)

            matches = [
                UMP.parse(match, standard_date)
                for match in sublist.css("div.match-zone-wrapper")
            ]

            all_upcoming_matches.extend(matches)

        return all_upcoming_matches