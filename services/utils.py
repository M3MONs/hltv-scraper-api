from flask import jsonify, current_app

def execute_spider(name: str, path: str, args: str):
    """Execute the spider with the given name and arguments."""
    sm = current_app.spider_manager
    sm.execute(name, path, args)
    return jsonify(sm.get_result(path))