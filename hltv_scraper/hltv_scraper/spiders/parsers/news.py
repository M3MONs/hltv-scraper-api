from typing import Any
from .parser import Parser

class NewsParser(Parser):
    @staticmethod
    def parse(articles) -> list[dict[str, Any]]:
        return [
        {
            "title": article.css(".newstext::text").get(),
            "img": article.css("img.newsflag::attr(src)").get(),
            "date": article.css("div.newsrecent::text").get(),
            "comments": article.css("div.newstc div:nth-child(2)::text").get(),
            "link": article.css("a::attr(href)").get(),
        }
        for article in articles
    ]