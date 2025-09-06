from .conditions import Condition, FileTimeCondition, JsonFileEmptyCondition, FileExistsCondition

class ConditionFactory:
    @staticmethod
    def get(condition_type, *args, **kwargs) -> Condition:
        if condition_type == 'file_time':
            return FileTimeCondition(*args, **kwargs)
        elif condition_type == 'json_file_empty':
            return JsonFileEmptyCondition(*args, **kwargs)
        elif condition_type == 'file_exists':
            return FileExistsCondition(*args, **kwargs)
        else:
            raise ValueError(f"Unknown condition type: {condition_type}")