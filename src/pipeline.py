import logging
import time
from src.config import API_KEY, STOCKS
from src.extract.api_extractor import APIExtractor
from src.transform.data_transformer import DataTransformer
from src.load.data_loader import DataLoader
from src.data_validator import DataValidator
from src.database import Database
from src.utils import send_alert


class StockDataPipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stocks = STOCKS
        
        # Initialize ETL components
        self.extractor = APIExtractor(API_KEY)
        self.transformer = DataTransformer()
        self.validator = DataValidator()
        self.database = Database()
        self.loader = DataLoader(self.database)
    
    def run(self):
        self.logger.info("Starting stock data collection pipeline")
        
        collected_data = []
        errors = []
        
        for symbol in self.stocks:
            # EXTRACT
            raw_data = self.extractor.extract_stock_data(symbol)
            time.sleep(15)  # Rate limiting
            
            if raw_data is None:
                errors.append(symbol)
                continue
            
            # TRANSFORM
            transformed_data = self.transformer.transform_stock_data(raw_data, symbol)
            if transformed_data is None:
                errors.append(symbol)
                continue
            
            # VALIDATE
            is_valid, validation_errors = self.validator.validate(transformed_data)
            if not is_valid:
                self.logger.error(f"Validation failed for {symbol}: {validation_errors}")
                errors.append(symbol)
                continue
            
            collected_data.append(transformed_data)
        
        # LOAD
        if collected_data:
            self.loader.load(collected_data)
            self.logger.info(f"Pipeline completed: {len(collected_data)}/{len(self.stocks)} stocks collected")
        else:
            self.logger.error("No valid data collected")
            send_alert("Pipeline failed: no valid data collected")
        
        if errors:
            self.logger.warning(f"Failed to collect: {', '.join(errors)}")