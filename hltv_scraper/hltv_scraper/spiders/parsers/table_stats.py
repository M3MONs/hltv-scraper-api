from typing import Any
from .parser import Parser
from .player_stats import PlayerStatsParser

class TableStatsParser(Parser):
    @staticmethod
    def parse(response) -> list[dict[str, Any]]:
        table_stats = response.css(".table.totalstats")
        return [
            {
                "team": table.css(".teamName.team::text").get(),
                "stats": PlayerStatsParser.parse(table.css("tr:not(.header-row)")),
            }
            for table in table_stats
        ]