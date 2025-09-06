from typing import Dict, Any
from datetime import datetime

from .spider_manager import SpiderManager


class HLTVScraper:
    _manager = None

    @classmethod
    def _get_manager(cls):
        if cls._manager is None:
            from config import BASE_DIR
            cls._manager = SpiderManager(BASE_DIR)
        return cls._manager

    @staticmethod
    def get_upcoming_matches() -> Dict[str, Any]:
        manager = HLTVScraper._get_manager()
        name = "hltv_upcoming_matches"
        path = "upcoming_matches"
        args = f"-o data/{path}.json"
        manager.execute(name, path, args)
        return manager.get_result(path)

    @staticmethod
    def get_match(id: str, match_name: str) -> Dict[str, Any]:
        manager = HLTVScraper._get_manager()
        name = "hltv_match"
        match_link = f"{id}/{match_name}"
        path = f"match/{id}_{match_name}"
        args = f"-a match={match_link} -o data/{path}.json"
        manager.execute(name, path, args)
        return manager.get_result(path)

    @staticmethod
    def get_team_rankings(type: str = "hltv", year: str = "", month: str = "", day: int = 0) -> Dict[str, Any]:
        manager = HLTVScraper._get_manager()
        name = "hltv_valve_ranking" if type == "valve" else "hltv_top30"
        path = f"rankings/{type}" if year == "" and month == "" and day == 0 else f"rankings/{type}_{year}_{month}_{day}"
        args = f"-a year={year} -a month={month} -a day={day} -o data/{path}.json"
        manager.execute(name, path, args)
        return manager.get_result(path)

    @staticmethod
    def search_team(name: str) -> Dict[str, Any]:
        manager = HLTVScraper._get_manager()
        name = name.lower()
        if not manager.is_profile("teams_profile", name):
            manager.run_spider("hltv_teams_search", name, f"-a team={name}")
        if not manager.is_profile("teams_profile", name):
            raise ValueError("Team not found!")
        return manager.get_profile("teams_profile", name)

    @staticmethod
    def get_team_matches(id: str, offset: int = 0) -> Dict[str, Any]:
        manager = HLTVScraper._get_manager()
        name = "hltv_team_matches"
        path = f"team_matches/{id}_{offset}"
        args = f"-a id={id} -a offset={offset} -o data/{path}.json"
        manager.execute(name, path, args)
        return manager.get_result(path)

    @staticmethod
    def get_team_profile(id: str, team_name: str) -> Dict[str, Any]:
        manager = HLTVScraper._get_manager()
        name = "hltv_team"
        path = f"team/{team_name}"
        args = f"-a team=/team/{id}/{team_name} -o data/{path}.json"
        manager.execute(name, path, args)
        return manager.get_result(path)

    @staticmethod
    def get_results(offset: int = 0) -> Dict[str, Any]:
        manager = HLTVScraper._get_manager()
        name = "hltv_results"
        path = f"results/results_{offset}"
        args = f"-a offset={offset} -o ./data/{path}.json"
        manager.execute(name, path, args)
        return manager.get_result(path)

    @staticmethod
    def get_big_results() -> Dict[str, Any]:
        manager = HLTVScraper._get_manager()
        name = "hltv_big_results"
        path = "big_results"
        args = f"-o data/{path}.json"
        manager.execute(name, path, args)
        return manager.get_result(path)

    @staticmethod
    def get_news(year: int = datetime.now().year, month: str = datetime.now().strftime("%B")) -> Dict[str, Any]:
        manager = HLTVScraper._get_manager()
        name = "hltv_news"
        path = f"news/news_{year}_{month}"
        args = f"-a year={year} -a month={month} -o data/{path}.json"
        manager.execute(name, path, args)
        return manager.get_result(path)

    @staticmethod
    def search_player(name: str) -> Dict[str, Any]:
        manager = HLTVScraper._get_manager()
        name = name.lower()
        if not manager.is_profile("players_profiles", name):
            manager.run_spider("hltv_players_search", name, f"-a player={name}")
        if not manager.is_profile("players_profiles", name):
            raise ValueError("Player not found!")
        return manager.get_profile("players_profiles", name)

    @staticmethod
    def get_player_profile(id: str, player_name: str) -> Dict[str, Any]:
        manager = HLTVScraper._get_manager()
        name = "hltv_player"
        path = f"player/{player_name}"
        args = f"-a profile=/player/{id}/{player_name} -o data/{path}.json"
        manager.execute(name, path, args)
        return manager.get_result(path)
