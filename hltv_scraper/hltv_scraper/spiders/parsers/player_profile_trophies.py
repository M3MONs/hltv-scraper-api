from typing import Any
from .parser import Parser

class PlayerProfileTrophiesParser(Parser):
    @staticmethod
    def parse(trophies) -> list[dict[str, Any]]:
        return [
        {
            "title": trophy.css("span.trophyDescription::attr(title)").get(),
            "icon": trophy.css("span.trophyDescription img::attr(src)").get(),
        }
        for trophy in trophies
    ]