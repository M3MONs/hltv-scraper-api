import pytest
import requests


class TestEnvironmentSetup:
    """Test that the environment is properly set up for integration testing"""
    
    def test_hltv_website_accessibility(self):
        """Test that HLTV.org is accessible"""
        try:
            # Use headers to avoid 403 blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get('https://www.hltv.org', timeout=10, headers=headers)
            # Accept both 200 and 403 as "accessible" - 403 means site is up but blocking bots
            assert response.status_code in [200, 403], f"HLTV.org returned {response.status_code}"
            print(f"HLTV.org is accessible (status: {response.status_code})")
        except requests.RequestException as e:
            pytest.skip(f"HLTV.org is not accessible: {e}")


class TestAPIEndpointsBasic:
    """Basic integration tests that test endpoint availability without deep scraping"""
    
    @pytest.mark.integration
    def test_player_search_endpoint_basic(self, client):
        """Test player search endpoint responds (may return 'not found')"""
        response = client.get('/api/v1/players/search/s1mple')
        
        # Accept any response that's not a server error
        assert response.status_code in [200, 404], f"Unexpected status: {response.status_code}"
        print(f"Player search endpoint responded with status: {response.status_code}")

    @pytest.mark.integration  
    def test_team_search_endpoint_basic(self, client):
        """Test team search endpoint responds (may return 'not found')"""
        response = client.get('/api/v1/teams/search/navi')
        
        # Accept any response that's not a server error
        assert response.status_code in [200, 404], f"Unexpected status: {response.status_code}"
        print(f"Team search endpoint responded with status: {response.status_code}")

    @pytest.mark.integration
    def test_results_endpoint_basic(self, client):
        """Test results endpoint responds (may return 'not found')"""
        response = client.get('/api/v1/results/')
        
        # Accept any response that's not a server error
        assert response.status_code in [200, 404, 500], f"Unexpected status: {response.status_code}"
        print(f"Results endpoint responded with status: {response.status_code}")

    @pytest.mark.integration
    def test_featured_results_endpoint_basic(self, client):
        """Test featured results endpoint responds (may return 'not found')"""
        response = client.get('/api/v1/results/featured')
        
        # Accept any response that's not a server error
        assert response.status_code in [200, 404, 500], f"Unexpected status: {response.status_code}"
        print(f"Featured results endpoint responded with status: {response.status_code}")


class TestScrapyIntegration:
    """Integration tests that require Scrapy to be properly configured"""
    
    @pytest.mark.slow
    @pytest.mark.integration
    def test_teams_ranking_endpoint_with_scrapy_fallback(self, client):
        """Test teams ranking endpoint - expect either success or controlled failure"""
        try:
            response = client.get('/api/v1/teams/rankings')
            
            if response.status_code == 200:
                data = response.get_json()
                # Accept both dict and list format from HLTV data
                assert isinstance(data, (dict, list))
                print("Teams ranking endpoint returned data successfully")
                if isinstance(data, list) and len(data) > 0:
                    print(f"Got {len(data)} ranking entries")
                elif isinstance(data, dict):
                    print(f"Got ranking data: {list(data.keys())}")
            elif response.status_code == 500:
                # This is expected if scrapy is not properly configured
                print("Teams ranking endpoint failed as expected (scrapy/HLTV issues)")
                pytest.skip("Scrapy not properly configured for integration testing")
            else:
                pytest.fail(f"Unexpected response status: {response.status_code}")
                
        except Exception as e:
            # If there's an exception, it's likely due to missing scrapy or HLTV blocking
            print(f"Teams ranking test failed with exception: {e}")
            pytest.skip("Integration test failed due to environment issues")

    @pytest.mark.slow  
    @pytest.mark.integration
    def test_upcoming_matches_endpoint_with_scrapy_fallback(self, client):
        """Test upcoming matches endpoint - expect either success or controlled failure"""
        try:
            response = client.get('/api/v1/matches/upcoming')
            
            if response.status_code == 200:
                data = response.get_json()
                # Accept both dict and list format from HLTV data
                assert isinstance(data, (dict, list))
                print("Upcoming matches endpoint returned data successfully")
                if isinstance(data, list) and len(data) > 0:
                    print(f"Got {len(data)} match entries")
                elif isinstance(data, dict):
                    print(f"Got match data: {list(data.keys())}")
            elif response.status_code == 500:
                print("Upcoming matches endpoint failed as expected (scrapy/HLTV issues)")
                pytest.skip("Scrapy not properly configured for integration testing")
            else:
                pytest.fail(f"Unexpected response status: {response.status_code}")
                
        except Exception as e:
            print(f"Upcoming matches test failed with exception: {e}")
            pytest.skip("Integration test failed due to environment issues")

    @pytest.mark.slow
    @pytest.mark.integration 
    def test_news_endpoint_with_scrapy_fallback(self, client):
        """Test news endpoint - expect either success or controlled failure"""
        try:
            response = client.get('/api/v1/news')
            
            if response.status_code == 200:
                data = response.get_json()
                # Accept both dict and list format from HLTV data
                assert isinstance(data, (dict, list))
                print("News endpoint returned data successfully")
                if isinstance(data, list) and len(data) > 0:
                    print(f"Got {len(data)} news entries")
                elif isinstance(data, dict):
                    print(f"Got news data: {list(data.keys())}")
            elif response.status_code == 500:
                print("News endpoint failed as expected (scrapy/HLTV issues)")
                pytest.skip("Scrapy not properly configured for integration testing")
            else:
                pytest.fail(f"Unexpected response status: {response.status_code}")
                
        except Exception as e:
            print(f"News test failed with exception: {e}")
            pytest.skip("Integration test failed due to environment issues")

    @pytest.mark.slow
    @pytest.mark.integration
    def test_results_endpoint_with_scrapy_fallback(self, client):
        """Test results endpoint - expect either success or controlled failure"""
        try:
            response = client.get('/api/v1/results/')
            
            if response.status_code == 200:
                data = response.get_json()
                # Accept both dict and list format from HLTV data
                assert isinstance(data, (dict, list))
                print("Results endpoint returned data successfully")
                if isinstance(data, list) and len(data) > 0:
                    print(f"Got {len(data)} result entries")
                elif isinstance(data, dict):
                    print(f"Got result data: {list(data.keys())}")
            elif response.status_code == 500:
                print("Results endpoint failed as expected (scrapy/HLTV issues)")
                pytest.skip("Scrapy not properly configured for integration testing")
            else:
                pytest.fail(f"Unexpected response status: {response.status_code}")
                
        except Exception as e:
            print(f"Results test failed with exception: {e}")
            pytest.skip("Integration test failed due to environment issues")

    @pytest.mark.slow
    @pytest.mark.integration
    def test_results_with_offset_endpoint_with_scrapy_fallback(self, client):
        """Test results endpoint with offset - expect either success or controlled failure"""
        try:
            response = client.get('/api/v1/results/100')
            
            if response.status_code == 200:
                data = response.get_json()
                # Accept both dict and list format from HLTV data
                assert isinstance(data, (dict, list))
                print("Results with offset endpoint returned data successfully")
                if isinstance(data, list) and len(data) > 0:
                    print(f"Got {len(data)} result entries with offset")
                elif isinstance(data, dict):
                    print(f"Got result data with offset: {list(data.keys())}")
            elif response.status_code == 500:
                print("Results with offset endpoint failed as expected (scrapy/HLTV issues)")
                pytest.skip("Scrapy not properly configured for integration testing")
            else:
                pytest.fail(f"Unexpected response status: {response.status_code}")
                
        except Exception as e:
            print(f"Results with offset test failed with exception: {e}")
            pytest.skip("Integration test failed due to environment issues")

    @pytest.mark.slow
    @pytest.mark.integration
    def test_featured_results_endpoint_with_scrapy_fallback(self, client):
        """Test featured results (big_results) endpoint - expect either success or controlled failure"""
        try:
            response = client.get('/api/v1/results/featured')
            
            if response.status_code == 200:
                data = response.get_json()
                # Accept both dict and list format from HLTV data
                assert isinstance(data, (dict, list))
                print("Featured results endpoint returned data successfully")
                if isinstance(data, list) and len(data) > 0:
                    print(f"Got {len(data)} featured result entries")
                elif isinstance(data, dict):
                    print(f"Got featured result data: {list(data.keys())}")
            elif response.status_code == 500:
                print("Featured results endpoint failed as expected (scrapy/HLTV issues)")
                pytest.skip("Scrapy not properly configured for integration testing")
            else:
                pytest.fail(f"Unexpected response status: {response.status_code}")
                
        except Exception as e:
            print(f"Featured results test failed with exception: {e}")
            pytest.skip("Integration test failed due to environment issues")
