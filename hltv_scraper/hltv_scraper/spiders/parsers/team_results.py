from typing import Any
from .parser import Parser

class TeamResultsParser(Parser):
    @staticmethod
    def parse(results) -> list[dict[str, Any]]:
        return [
        {
            "team1": {
                "name": result.css(".team1 .team::text").get(),
                "logo": result.css(".team1 img::attr(src)").get(),
            },
            "team2": {
                "name": result.css(".team2 .team::text").get(),
                "logo": result.css(".team2 img::attr(src)").get(),
            },
            "event": result.css(".event-name::text").get(),
            "score": result.css(".result-score ::text").getall(),
            "map": results.css(".map.map-text::text").get(),
            "link": result.css("a.a-reset::attr(href)").get(),
        }
        for result in results
    ]