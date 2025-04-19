import re
from abc import ABC, abstractmethod
from datetime import datetime

class DateFormatter(ABC):
    @abstractmethod
    def format(self, date: str) -> str:
        pass


class ResultDateFormatter(DateFormatter):
    @staticmethod
    def format(date: str) -> str:
        match_date = re.search(r'(\w+)\s(\d+)[a-z]{2}\s(\d{4})', date)
        month, day, year = match_date.groups()
        date_obj = datetime.strptime(f"{month} {day} {year}", "%B %d %Y")
        standard_date = date_obj.strftime("%Y-%m-%d")
        return standard_date