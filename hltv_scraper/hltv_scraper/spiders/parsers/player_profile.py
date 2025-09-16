from typing import Any
from .parser import Parser
from .player_profile_trophies import PlayerProfileTrophiesParser as PPTP
from .player_profile_stats import PlayerProfileStatsParser as PPSP


class PlayerProfileParser(Parser):
    @staticmethod
    def parse(profile) -> dict[str, Any]:
        return {
            "nick": profile.css("h1.playerNickname::text").get(),
            "name": profile.css("div.playerRealname::text").get(),
            "flag": profile.css("div.playerRealname img::attr(src)").get(),
            "team": profile.css('div.playerTeam span[itemprop="text"] ::text').getall(),
            "stats": PPSP.parse(profile.css("div.player-stat")),
            "trophies": PPTP.parse(profile.css(".trophy")),
        }
