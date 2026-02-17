import logging
from datetime import datetime


class DataTransformer:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def transform_stock_data(self, raw_data, symbol):
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