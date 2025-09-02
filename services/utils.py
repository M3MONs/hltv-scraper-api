from flask import jsonify, current_app
from typing import Any, cast

def execute_spider(name: str, path: str, args: str):
    """Execute the spider with the given name and arguments."""
    sm = cast(Any, current_app).spider_manager
    
    sm.execute(name, path, args)
    return jsonify(sm.get_result(path))