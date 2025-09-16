from typing import Any
from .parser import Parser

class PlayerProfileLinkParser(Parser):
    @staticmethod
    def parse(response, player: str) -> Any:
        return response.css(f"a[href^='/player/'][href$='/{player}']").getall()
        