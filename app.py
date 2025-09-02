from flask import Flask
from config import BASE_DIR
from services.spider_manager import SpiderManager

def create_app():
    app = Flask(__name__)
    
    app.json.sort_keys = False # type: ignore
    
    app.spider_manager = SpiderManager(BASE_DIR) # type: ignore

    from routes.teams import teams_bp
    from routes.players import players_bp
    from routes.matches import matches_bp
    from routes.news import news_bp
    from routes.results import results_bp

    app.register_blueprint(teams_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(results_bp)

    return app

flask_app = create_app()

if __name__ == "__main__":
    flask_app.run(debug=True, host='0.0.0.0', port=8000)