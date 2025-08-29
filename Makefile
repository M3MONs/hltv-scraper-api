.PHONY: test test-working test-cov test-unit test-integration test-slow clean install

# Install dependencies
install:
	./env/bin/pip install pytest pytest-flask pytest-cov requests

# Run all tests (unit + integration)
test:
	./env/bin/python -m pytest tests/ -v

# Run only unit tests (fast, with mocks)
test-unit:
	./env/bin/python -m pytest tests/test_routes.py -v

# Run only integration tests (slow, real HLTV connections)
test-integration:
	./env/bin/python -m pytest tests/test_integration_real.py -v

# Run only fast tests (exclude slow integration tests)
test-fast:
	./env/bin/python -m pytest -m "not slow" tests/ -v

# Run only slow tests (integration tests)
test-slow:
	./env/bin/python -m pytest -m "slow" tests/ -v

# Run tests with coverage report
test-cov:
	./env/bin/python -m pytest --cov=routes --cov-report=html --cov-report=term tests/

# Clean cache and temp files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -name "*.pyc" -delete
	rm -rf htmlcov/

# Run specific test
test-one:
	./env/bin/python -m pytest tests/test_routes.py::TestRoutesEndpoints::$(TEST) -v
