import scrapy
from .parsers import ParsersFactory as PF


class HltvValveRankingSpider(scrapy.Spider):
    name = "hltv_valve_ranking"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/valve-ranking/teams"]

    def parse(self, response):
        ranked_teams = response.css("div.ranked-team.standard-box")

        for team in ranked_teams:
            data = PF.get_parser("team_ranking").parse(team)
            yield data
