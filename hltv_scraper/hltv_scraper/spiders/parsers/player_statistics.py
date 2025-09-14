from typing import Any, List, Dict
from .parser import Parser

class PlayerStatisticsParser(Parser):
    @staticmethod
    def parse(statistics_box: Any) -> List[Dict[str, str]]:
        return [
            {
                "title": spans[0].strip(),
                "value": spans[1].strip()
            }
            for row in statistics_box.css('div.stats-row')
            if (spans := row.css('span::text').getall()) and len(spans) >= 2
        ]
