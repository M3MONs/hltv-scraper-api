from typing import Any
from .parser import Parser

class MapHoldersParser(Parser):
    @staticmethod
    def parse(response) -> list[dict[str, Any]]:
        map_holders = response.css(".match-page .mapholder")
        team1 = map_holders.css(".results-left .results-teamname::text").get()
        team2 = map_holders.css(".results-right .results-teamname::text").get()
        return [
            {
                "map_img": map.css(".map-name-holder img::attr(src)").get(),
                "map_name": map.css(".map-name-holder .mapname::text").get(),
                "score": {
                    f"{team1}": map.css(".results-left .results-team-score::text").get(),
                    f"{team2}": map.css(".results-right .results-team-score::text").get(),
                },
            }
            for map in map_holders
        ]