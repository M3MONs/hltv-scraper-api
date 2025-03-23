from abc import ABC, abstractmethod
import json
import os


class DataLoader(ABC):
    @abstractmethod
    def load(self, file: str) -> dict:
        pass


class JsonDataLoader(DataLoader):
    def load(self, file: str) -> dict:
        try:
            if not os.path.exists(file):
                return {}
                
            with open(file, "r") as json_file:
                return json.load(json_file)
        except Exception as e:
            print(f"Error loading JSON file {file}: {e}")
            return {}
