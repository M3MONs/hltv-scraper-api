from .conditions import Condition
from abc import ABC, abstractmethod


class Checker(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass
    
    @abstractmethod
    def check(self) -> bool:
        pass

# Check if any of the conditions are met
class AnyConditionsChecker(Checker):
    def __init__(self, conditions: list[Condition]) -> None:
        self.conditions = conditions

    def check(self) -> bool:
        for condition in self.conditions:
            print(f"Checking condition: {condition} -> {condition.check()}")
            if condition.check():
                return True
        return False
