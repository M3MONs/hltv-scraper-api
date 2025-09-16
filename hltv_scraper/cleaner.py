from abc import ABC
from typing import Any


class OldDataCleaner(ABC):
    @staticmethod
    def clean(_: Any) -> None:
        pass


class JsonOldDataCleaner(OldDataCleaner):
    @staticmethod
    def clean(file: str) -> None:
        open(file, "w").close()
