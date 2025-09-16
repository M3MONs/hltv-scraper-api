from typing import Any
from .parser import Parser

class PlayerStatsParser(Parser):
    @staticmethod
    def parse(players) -> list[dict[str, Any]]:
        return [
        {
            "img": player.css(".flag.flag::attr(src)").get(),
            "name": " ".join(
                player.css(".gtSmartphone-only.statsPlayerName ::text").getall()
            ),
            "kd": player.css(".kd::text").get(),
            "+/-": player.css(".plus-minus ::text").get(),
            "adr": player.css(".adr::text").get(),
            "swing": player.css(".roundSwing::text").get(),
            "rating 3.0": player.css(".rating::text").get(),
        }
        for player in players
    ]