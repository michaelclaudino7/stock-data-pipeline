import pandas as pd
import logging
import os
from datetime import datetime
from src.config import DATA_DIR
from src.utils import send_alert


class DataLoader:
    
    def __init__(self, database):
        self.db = database
        self.logger = logging.getLogger(__name__)
    
    def load_to_database(self, data):
        try:
            self.db.insert_stock_price(data)
        except Exception as e:
            self.logger.error(f"Failed to load {data['symbol']} to database: {e}")
            raise
    
    def load_to_csv(self, data_list):
        if not data_list:
            return
        
        try:
            df = pd.DataFrame(data_list)
            date_str = datetime.now().strftime('%Y%m%d')
            filename = f"stock_data_{date_str}.csv"
            filepath = os.path.join(DATA_DIR, filename)
            
            if os.path.exists(filepath):
                df.to_csv(filepath, mode='a', header=False, index=False)
            else:
                df.to_csv(filepath, index=False)
                
            self.logger.info(f"Data saved to {filename}")
                
        except Exception as e:
            self.logger.error(f"Failed to save CSV: {e}")
    
    def load(self, data_list):
        if not data_list:
            self.logger.warning("No data to load")
            return
        
        try:
            # Load to database
            for data in data_list:
                self.load_to_database(data)
            
            # Load to CSV backup
            self.load_to_csv(data_list)
            
            self.logger.info(f"Successfully loaded {len(data_list)} records")
            
        except Exception as e:
            self.logger.error(f"Load failed: {e}")
            send_alert(f"Failed to load data: {e}")