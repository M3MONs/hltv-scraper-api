from typing import Any
from .parser import Parser


class TeamParser(Parser):
    @staticmethod
    def parse(result, number) -> dict[str, Any]:
        return {
            "name": result.css(f"div.team{number} .team::text").get(),
            "score": result.css(
                f"td.result-score span:nth-child({number})::text"
            ).get(),
            "logo": result.css(f"div.team{number} img::attr(src)").get(),
        }
