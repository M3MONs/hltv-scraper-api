from .date import ResultDateFormatter
from .parser import Parser
from .match import MatchParser as MP

class ResultsParser(Parser):
    @staticmethod
    def parse(sublists):
        all_results = []
        for sublist in sublists:
            date = sublist.css(".standard-headline::text").get()
            standard_date = None
            if date:
                standard_date = ResultDateFormatter.format(date)
            
            matches = [MP.parse(result, standard_date) for result in sublist.css("a.a-reset")]
            all_results.extend(matches)
        return all_results