import json
from unittest.mock import Mock, patch


class TestRoutesEndpoints:
    """Tests for all API route endpoints."""

    def test_teams_ranking_endpoint(self, client, app):
        """Test teams ranking endpoint."""
        mock_data = {"teams": ["Natus Vincere", "Astralis", "FaZe Clan"]}
        
        with app.app_context():
            with patch('services.utils.current_app') as mock_current_app:
                mock_spider_manager = Mock()
                mock_spider_manager.execute.return_value = None
                mock_spider_manager.get_result.return_value = mock_data
                mock_current_app.spider_manager = mock_spider_manager
                
                response = client.get('/api/v1/teams/rankings')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert isinstance(data, dict)
                assert data == mock_data

    def test_upcoming_matches_endpoint(self, client, app):
        """Test upcoming matches endpoint."""
        mock_data = {"matches": [{"team1": "NAVI", "team2": "Astralis", "date": "2023-08-30"}]}
        
        with app.app_context():
            with patch('services.utils.current_app') as mock_current_app:
                mock_spider_manager = Mock()
                mock_spider_manager.execute.return_value = None
                mock_spider_manager.get_result.return_value = mock_data
                mock_current_app.spider_manager = mock_spider_manager
                
                response = client.get('/api/v1/matches/upcoming')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert isinstance(data, dict)
                assert data == mock_data

    def test_news_endpoint(self, client, app):
        """Test news endpoint."""
        mock_data = {"news": [{"title": "Major tournament announced", "date": "2023-08-30"}]}
        
        with app.app_context():
            with patch('services.utils.current_app') as mock_current_app:
                mock_spider_manager = Mock()
                mock_spider_manager.execute.return_value = None
                mock_spider_manager.get_result.return_value = mock_data
                mock_current_app.spider_manager = mock_spider_manager
                
                response = client.get('/api/v1/news')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert isinstance(data, dict)
                assert data == mock_data

    def test_results_endpoint(self, client, app):
        """Test results endpoint."""
        mock_data = {"results": [{"team1": "NAVI", "team2": "Astralis", "score": "16-14"}]}
        
        with app.app_context():
            with patch('services.utils.current_app') as mock_current_app:
                mock_spider_manager = Mock()
                mock_spider_manager.execute.return_value = None
                mock_spider_manager.get_result.return_value = mock_data
                mock_current_app.spider_manager = mock_spider_manager
                
                response = client.get('/api/v1/results/')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert isinstance(data, dict)
                assert data == mock_data

    def test_player_search_success(self, client, app):
        """Test player search with successful result."""
        mock_data = {"player": "s1mple", "team": "NAVI", "rating": 1.25}
        
        with app.app_context():
            with patch('routes.players.current_app') as mock_current_app:
                mock_spider_manager = Mock()
                mock_spider_manager.is_profile.return_value = True
                mock_spider_manager.get_profile.return_value = mock_data
                mock_current_app.spider_manager = mock_spider_manager
                
                response = client.get('/api/v1/players/search/s1mple')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data == mock_data

    def test_player_search_not_found(self, client, app):
        """Test player search when player is not found."""
        with app.app_context():
            with patch('routes.players.current_app') as mock_current_app:
                mock_spider_manager = Mock()
                mock_spider_manager.is_profile.return_value = False
                mock_current_app.spider_manager = mock_spider_manager
                
                response = client.get('/api/v1/players/search/nonexistent')
                
                assert response.status_code == 200
                assert response.data == b"Player not found!"

    def test_team_search_success(self, client, app):
        """Test team search with successful result."""
        mock_data = {"team": "NAVI", "country": "Ukraine", "players": ["s1mple", "electronic"]}
        
        with app.app_context():
            with patch('routes.teams.current_app') as mock_current_app:
                mock_spider_manager = Mock()
                mock_spider_manager.is_profile.return_value = True
                mock_spider_manager.get_profile.return_value = mock_data
                mock_current_app.spider_manager = mock_spider_manager
                
                response = client.get('/api/v1/teams/search/navi')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert data == mock_data

    def test_team_search_not_found(self, client, app):
        """Test team search when team is not found."""
        with app.app_context():
            with patch('routes.teams.current_app') as mock_current_app:
                mock_spider_manager = Mock()
                mock_spider_manager.is_profile.return_value = False
                mock_current_app.spider_manager = mock_spider_manager
                
                response = client.get('/api/v1/teams/search/nonexistent')
                
                assert response.status_code == 404
                data = json.loads(response.data)
                assert data == {"error": "Team not found!"}
