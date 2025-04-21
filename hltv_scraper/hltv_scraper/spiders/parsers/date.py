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
        match_date = re.search(r"(\w+)\s(\d+)[a-z]{2}\s(\d{4})", date)
        month, day, year = match_date.groups()
        date_obj = datetime.strptime(f"{month} {day} {year}", "%B %d %Y")
        standard_date = date_obj.strftime("%Y-%m-%d")
        return standard_date


class RankingDateFormatter(DateFormatter):
    @staticmethod
    # date format: "Counter-Strike World ranking on April 14th, 2025" or "Valve global ranking on April 21st, 2025"
    def format(date: str) -> str:
        match_date = re.search(r"on\s(\w+\s\d+)", date)
        month_day = match_date.group(1)

        month, day = month_day.split()
        year = date.strip()[-4:]

        print(f"date: {date}, month: {month}, day: {day}, year: {year}")

        date_obj = datetime.strptime(f"{month} {day} {year}", "%B %d %Y")
        standard_date = date_obj.strftime("%Y-%m-%d")
        return standard_date


# TODO: Implement date formatter for upcoming matches
