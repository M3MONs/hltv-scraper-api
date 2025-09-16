from abc import ABC, abstractmethod

class Parser(ABC):
    @abstractmethod
    def parse(*args, **kwargs) -> None:
        pass