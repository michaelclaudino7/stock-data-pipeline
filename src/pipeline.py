import requests
import pandas as pd
import logging
from datetime import datetime
import os
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.config import API_KEY, STOCKS, DATA_DIR, LOG_DIR
from src.data_validator import DataValidator
from src.utils import setup_logging, send_alert


class StockDataPipeline:
    
    def __init__(self):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = API_KEY
        self.stocks = STOCKS
        self.logger = logging.getLogger(__name__)
        self.validator = DataValidator()
        
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
    
    def transform_data(self, raw_data, symbol):
        try:
            transformed = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'symbol': symbol,
                'price': float(raw_data.get('05. price', 0)),
                'volume': int(raw_data.get('06. volume', 0)),
                'latest_trading_day': raw_data.get('07. latest trading day', ''),
                'previous_close': float(raw_data.get('08. previous close', 0)),
                'change': float(raw_data.get('09. change', 0)),
                'change_percent': raw_data.get('10. change percent', '0%').replace('%', '')
            }
            
            self.logger.info(f"{symbol}: ${transformed['price']}")
            return transformed
            
        except Exception as e:
            self.logger.error(f"Transform failed for {symbol}: {e}")
            return None
    
    def load_data(self, data_list):
        if not data_list:
            self.logger.warning("No data to load")
            return
        
        try:
            df = pd.DataFrame(data_list)
            
            date_str = datetime.now().strftime('%Y%m%d')
            filename = f"stock_data_{date_str}.csv"
            filepath = os.path.join(DATA_DIR, filename)
            
            if os.path.exists(filepath):
                df.to_csv(filepath, mode='a', header=False, index=False)
                self.logger.info(f"Data appended to {filename}")
            else:
                df.to_csv(filepath, index=False)
                self.logger.info(f"Created {filename}")
                
            history_file = os.path.join(DATA_DIR, "stock_data_history.csv")
            if os.path.exists(history_file):
                df.to_csv(history_file, mode='a', header=False, index=False)
            else:
                df.to_csv(history_file, index=False)
                
        except Exception as e:
            self.logger.error(f"Save failed: {e}")
            send_alert(f"Failed to save data: {e}")
    
    def run(self):
        self.logger.info("Starting stock data collection pipeline")
        
        collected_data = []
        errors = []
        
        for symbol in self.stocks:
            raw_data = self.extract_stock_data(symbol)
            time.sleep(15)
            if raw_data is None:
                errors.append(symbol)
                continue
            
            transformed_data = self.transform_data(raw_data, symbol)
            if transformed_data is None:
                errors.append(symbol)
                continue
            
            is_valid, validation_errors = self.validator.validate(transformed_data)
            if not is_valid:
                self.logger.error(f"Validation failed for {symbol}: {validation_errors}")
                errors.append(symbol)
                continue
            
            collected_data.append(transformed_data)
        
        if collected_data:
            self.load_data(collected_data)
            self.logger.info(f"Pipeline completed: {len(collected_data)}/{len(self.stocks)} stocks collected")
        else:
            self.logger.error("No valid data collected")
            send_alert("Pipeline failed: no valid data collected")
        
        if errors:
            self.logger.warning(f"Failed to collect: {', '.join(errors)}")


if __name__ == "__main__":
    setup_logging()
    pipeline = StockDataPipeline()
    pipeline.run()
