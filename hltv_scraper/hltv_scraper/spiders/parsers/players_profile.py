from typing import Any
import scrapy
from .parser import Parser

class PlayersProfileParser(Parser):
    @staticmethod
    def parse(profiles) -> list[dict[str, Any]]:
        profiles_data = []
        for profile in profiles:
            selector = scrapy.Selector(text=profile)
            data = {
                "name": selector.css("a::text").get(),
                "profile_link": selector.css("a::attr(href)").get(),
                "img": selector.css("img::attr(src)").get(),
            }
            profiles_data.append(data)
        return profiles_data    