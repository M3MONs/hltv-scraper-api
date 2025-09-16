from typing import Any, Generator
import scrapy

from .parsers.date import RankingDateFormatter
from .parsers import ParsersFactory as PF


class HltvTop30Spider(scrapy.Spider):
    name = "hltv_top30"
    allowed_domains = ["www.hltv.org"]

    def __init__(self, year=None, month=None, day=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if year != "" and month != "" and day != 0:
            self.start_urls = [f"https://www.hltv.org/ranking/teams/{year}/{month}/{day}"]
        else:
            self.start_urls = ["https://www.hltv.org/ranking/teams"]

    def parse(self, response) -> Generator[dict[str, Any], Any, None]:
        ranked_teams = response.css("div.ranked-team.standard-box")
        prev_ranking = response.css("div.ranking-prev-next a.pagination-prev::attr(href)").re_first(r"/ranking/teams/(\d{4}/\w+/\d+)")
        next_ranking = response.css("div.ranking-prev-next a.pagination-next::attr(href)").re_first(r"/ranking/teams/(\d{4}/\w+/\d+)")
        date_text = response.css("div.regional-ranking-header-text::text").get()
        parsed_date = RankingDateFormatter.format(date_text)

        data = {
            "date": parsed_date,
            "prev_ranking": prev_ranking if prev_ranking else None,
            "next_ranking": next_ranking if next_ranking else None,
            "ranking_type": "hltv",
            "ranking": [],
        }

        for team in ranked_teams:
            team_data = PF.get_parser("team_ranking").parse(team)
            data["ranking"].append(team_data)

        yield data
