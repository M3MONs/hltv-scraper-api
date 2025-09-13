from typing import Any, Dict, List, Optional
from .parser import Parser


class PlayerRoleStatsParser(Parser):
    @staticmethod
    def parse(role_stats_container: Any) -> Dict[str, Dict]:
        stat_sections = role_stats_container.css("div.role-stats-section")
        data = {}

        for section in stat_sections:
            stat_data = PlayerRoleStatsParser._parse_stat_section(section)
            if stat_data:
                data[stat_data["title"]] = stat_data

        return data

    @staticmethod
    def _parse_stat_section(section: Any) -> Optional[Dict[str, Any]]:
        main_title_raw = section.xpath('normalize-space(.//div[@class="role-stats-section-title"]/text()[normalize-space()][1])').get()
        main_title = main_title_raw.strip() if main_title_raw else ""

        main_score_raw = section.xpath('string(.//div[@class="row-stats-section-score"])').get()
        main_score = main_score_raw.strip() if main_score_raw else ""

        detail_stats = PlayerRoleStatsParser._extract_detail_stats(section)

        if not main_title:
            return None

        return {"title": main_title, "main_score": main_score, "details": detail_stats}

    @staticmethod
    def _extract_detail_stats(section: Any) -> List[Dict[str, str]]:
        detail_rows = section.css("div.role-stats-row.stats-side-combined")
        details = []

        for row in detail_rows:
            title_raw = row.xpath('string(.//div[@class="role-stats-title"])').get()
            value_raw = row.xpath('string(.//div[@class="role-stats-data"])').get()

            if title_raw and value_raw:
                details.append({"title": title_raw.strip(), "value": value_raw.strip()})

        return details
