from typing import Any, Dict, Optional
from .parser import Parser


class PlayerSummaryStatParser(Parser):
    @staticmethod
    def parse(summary_stat_box: Any) -> Dict[str, Any]:
        t_rating_value, ct_rating_value = PlayerSummaryStatParser._extract_side_ratings(summary_stat_box)
        summary_stats = PlayerSummaryStatParser._extract_summary_stats(summary_stat_box)

        return {
            "rating": summary_stat_box.css("div.player-summary-stat-box-rating-data-text::text").get(),
            "rating_text": summary_stat_box.css("div.player-summary-stat-box-rating-text::text").get(),
            "t_rating": t_rating_value,
            "ct_rating": ct_rating_value,
            "summary_stats": summary_stats,
        }

    @staticmethod
    def _extract_side_ratings(summary_stat_box: Any) -> tuple[Optional[str], Optional[str]]:
        rating_wrapper_text = summary_stat_box.css("div.player-summary-stat-box-side-rating-background-wrapper::text").getall()
        cleaned_rating_text = [text.strip() for text in rating_wrapper_text if text.strip()]
        
        t_rating_value = cleaned_rating_text[0] if cleaned_rating_text else None
        ct_rating_value = cleaned_rating_text[1] if len(cleaned_rating_text) > 1 else None
        return t_rating_value, ct_rating_value

    @staticmethod
    def _extract_summary_stats(summary_stat_box: Any) -> Dict[str, Dict[str, Optional[str]]]:
        summary_stats = {}
        data_wrappers = summary_stat_box.css("div.player-summary-stat-box-right-bottom div.player-summary-stat-box-data-wrapper")
        for wrapper in data_wrappers:
            stat = PlayerSummaryStatParser._parse_stat_wrapper(wrapper)
            if stat:
                summary_stats[stat['name']] = {'value': stat['value'], 'description': stat['description']}
        return summary_stats

    @staticmethod
    def _parse_stat_wrapper(wrapper: Any) -> Optional[Dict[str, Optional[str]]]:
        """
        Parse a single stat wrapper to extract name, value, and description.
        """
        name_elem = wrapper.css("div.player-summary-stat-box-data-text")
        name = name_elem.xpath('text()').get()
        if not name:
            return None
        name = name.strip()

        value_elem = wrapper.css("div.player-summary-stat-box-data")
        value = value_elem.xpath('text()').get()
        if value:
            value = value.strip()
            if '%' in value:
                value = value.replace('%', '')
            if value == '-':
                value = None
        else:
            value = None

        desc_elem = wrapper.css("div.player-summary-stat-box-breakdown-description")
        description = desc_elem.xpath('text()').get()
        if description:
            description = description.strip()
        else:
            description = None

        return {'name': name, 'value': value, 'description': description}
