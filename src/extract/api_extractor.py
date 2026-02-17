import requests
import logging


class APIExtractor:
    
    def __init__(self, api_key):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
    
    def extract_stock_data(self, symbol):
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            self.logger.info(f"Fetching data for {symbol}")
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'Global Quote' not in data or not data['Global Quote']:
                self.logger.warning(f"No data available for {symbol}")
                return None
                
            return data['Global Quote']
            
        except Exception as e:
            self.logger.error(f"Failed to fetch {symbol}: {e}")
            return None