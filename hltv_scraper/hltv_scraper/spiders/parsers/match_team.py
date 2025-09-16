from typing import Any
from .parser import Parser


class MatchTeamParser(Parser):
    @staticmethod
    def parse(teams_box, number: int) -> dict[str, Any]:
        return {
            "name": teams_box.css(f"div.team{number}-gradient .teamName::text").get(),
            "logo": teams_box.css(f"div.team{number}-gradient img::attr(src)").get(),
            "score": teams_box.css(
                f".team{number}-gradient > div:nth-child(2)::text"
            ).get(),
        }
