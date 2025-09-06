import os
import time
import json
from abc import ABC, abstractmethod


class Condition(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass
    
    @abstractmethod
    def check(self) -> bool:
        pass

# Check if a file is older than a certain number of hours
class FileTimeCondition(Condition):
    def __init__(self, file_path: str, hours: int = 1) -> None:
        self.file_path = file_path
        self.hours = hours
    
    def check(self) -> bool:
        if not os.path.exists(self.file_path):
            return True
        file_age_in_seconds = time.time() - os.path.getmtime(self.file_path)
        return file_age_in_seconds > (3600 * self.hours)


class JsonFileEmptyCondition(Condition):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        
    def check(self) -> bool:
        if not os.path.exists(self.file_path):
            return True

        try:
            with open(self.file_path, "r") as file:
                file_data = json.load(file)
                return file_data == []
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return True
        
class FileExistsCondition(Condition):
    def __init__(self, file_path:str) -> None:
        self.file_path = file_path
        
    def check(self) -> bool:
        return os.path.exists(self.file_path)
