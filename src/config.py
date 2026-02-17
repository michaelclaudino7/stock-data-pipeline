import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')

# Stocks to monitor
STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.path.join(LOG_DIR, 'pipeline.log')

# Validation thresholds
MIN_PRICE = 0.01
MAX_PRICE = 1000000
MIN_VOLUME = 0