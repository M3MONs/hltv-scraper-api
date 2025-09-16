from typing import Any
from .parser import Parser

class SingleTeamParser(Parser):
    @staticmethod
    def parse(match, name: int, child: int) -> dict[str, Any]:
        return {
            "name": match.css(f".team-flex :nth-child({name})::text").get(),
            "logo": match.css(f".team-flex:nth-child({child}) .team-logo::attr(src)").get(),
            "score": match.css(f".score:nth-child({child})::text").get(),
        }