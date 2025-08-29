import pytest
import os
import sys

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app


@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    # Set up PATH to include virtual environment for scrapy
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    venv_bin_path = os.path.join(project_root, "env", "bin")
    current_path = os.environ.get('PATH', '')
    if venv_bin_path not in current_path:
        os.environ['PATH'] = f"{venv_bin_path}:{current_path}"
    
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })
    
    # Create an application context
    ctx = app.app_context()
    ctx.push()
    
    yield app
    
    ctx.pop()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
