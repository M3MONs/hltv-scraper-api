import os
import datetime

API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

BASE_DIR = "./hltv_scraper"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

DEFAULT_RATE_LIMIT = "1 per second"

TODAY = datetime.date.today()