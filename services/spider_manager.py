from abc import ABC, abstractmethod
from typing import List

from classes import (
    OldDataCleaner,
    ConditionsChecker,
    JsonOldDataCleaner,
    JsonDataLoader,
    JsonFilePathGenerator,
    FilePathGenerator,
    SpiderProcess,
    DataLoader,
    ConditionFactory as CF,
)


class Manager(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __get_conditions__(self, path: str, hours: int = 1) -> List:
        pass

    @abstractmethod
    def __should_run__(self, path: str) -> bool:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def get_result(self) -> dict:
        pass
    
    @abstractmethod
    def get_profile(self) -> dict:
        pass
    
    @abstractmethod
    def is_profile(self) -> bool:
        pass
    
    @abstractmethod
    def run_spider(self) -> None:
        pass


class SpiderManager(Manager):
    def __init__(self, dir: str) -> None:
        self.loader: DataLoader = JsonDataLoader()
        self.path: FilePathGenerator = JsonFilePathGenerator(dir)
        self.cleaner: OldDataCleaner = JsonOldDataCleaner()
        self.dir: str = dir

    def __get_conditions__(self, path: str, hours: int = 1) -> List:
        return [
            CF.get("file_time", file_path=path, hours=hours),
            CF.get("json_file_empty", file_path=path),
        ]

    def __should_run__(self, path: str) -> bool:
        conditions = self.__get_conditions__(path)
        checker = ConditionsChecker(conditions)
        return checker.check()

    def run_spider(self, name: str, path: str, args: str) -> None:
        path = self.path.generate(path)
        if CF.get("file_exists", file_path=path).check():
            self.cleaner.clean(path)
        SpiderProcess().execute(name, self.dir, args)

    def execute(self, name: str, path: str, args: str) -> None:
        path = self.path.generate(path)
        if self.__should_run__(path):
            if CF.get("file_exists", file_path=path).check():
                self.cleaner.clean(path)
            SpiderProcess().execute(name, self.dir, args)

    def get_result(self, path: str) -> dict:
        return self.loader.load(self.path.generate(path))

    def get_profile(self, filename: str, profile: str) -> dict:
        path = self.path.generate(filename)
        profiles = self.loader.load(path)
        return profiles[profile]

    def is_profile(self, filename: str, profile: str) -> bool:
        path = self.path.generate(filename)
        if not CF.get("file_exists", file_path=path).check():
            return False
        profiles = self.loader.load(path)
        return profile in profiles
