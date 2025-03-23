from .parser import Parser

class UpcomingMatchTeamParser(Parser):
    @staticmethod
    def parse(match, number):
        return {
            "name": match.css(f"div.team{number} .match-teamname::text").get(),
            "logo": match.css(f"div.team{number} img::attr(src)").get(),
        }
