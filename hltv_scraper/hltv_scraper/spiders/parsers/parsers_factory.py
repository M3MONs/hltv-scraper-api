from .parser import Parser
from .match import MatchParser
from .team import TeamParser
from .team_ranking import TeamRankingParser
from .upcoming_match_team import UpcomingMatchTeamParser
from .map_holders import MapHoldersParser
from .match_team import MatchTeamParser
from .match_teams_box import MatchTeamsBoxParser
from .table_stats import TableStatsParser
from .news import NewsParser
from .player_profile import PlayerProfileParser
from .player_profile_link import PlayerProfileLinkParser
from .players_profile import PlayersProfileParser
from .results import ResultsParser
from .team_results import TeamResultsParser
from .team_profile import TeamProfileParser
from .teams_profile_link import TeamProfileLinkParser
from .upcoming_match import UpcomingMatchParser
from .upcoming_matches import UpcomingMatchesParser
from .player_sumary_stats import PlayerSummaryStatParser
from .player_statistics import PlayerStatisticsParser
from .player_role_stats import PlayerRoleStatsParser

class ParsersFactory:
    @staticmethod
    def get_parser(parser_name: str) -> Parser:
        if parser_name == "match":
            return MatchParser()
        elif parser_name == "team":
            return TeamParser()
        elif parser_name == "team_ranking":
            return TeamRankingParser()
        elif parser_name == "upcoming_match_team":
            return UpcomingMatchTeamParser()
        elif parser_name == "map_holders":
            return MapHoldersParser()
        elif parser_name == "match_team":
            return MatchTeamParser()
        elif parser_name == "match_teams_box":
            return MatchTeamsBoxParser()
        elif parser_name == "table_stats":
            return TableStatsParser()
        elif parser_name == "news":
            return NewsParser()
        elif parser_name == "player_profile":
            return PlayerProfileParser()
        elif parser_name == "player_profile_link":
            return PlayerProfileLinkParser()
        elif parser_name == "players_profile":
            return PlayersProfileParser()
        elif parser_name == "results":
            return ResultsParser()
        elif parser_name == "team_results":
            return TeamResultsParser()
        elif parser_name == "team_profile":
            return TeamProfileParser()
        elif parser_name == "teams_profile_link":
            return TeamProfileLinkParser()
        elif parser_name == "upcoming_match":
            return UpcomingMatchParser()
        elif parser_name == "upcoming_matches":
            return UpcomingMatchesParser()
        elif parser_name == "player_summary_stats":
            return PlayerSummaryStatParser()
        elif parser_name == "player_statistics":
            return PlayerStatisticsParser()
        elif parser_name == "player_role_stats":
            return PlayerRoleStatsParser()
        else:
            raise ValueError(f"Unknown parser name: {parser_name}")