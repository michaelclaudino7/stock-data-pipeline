import logging
from src.config import MIN_PRICE, MAX_PRICE, MIN_VOLUME


class DataValidator:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate(self, data):
        """Validate stock data record"""
        errors = []
        
        # Check required fields
        required_fields = ['timestamp', 'symbol', 'price', 'volume']
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return False, errors
        
        # Validate price
        try:
            price = float(data['price'])
            if price < MIN_PRICE or price > MAX_PRICE:
                errors.append(f"Price out of range: ${price}")
        except (ValueError, TypeError):
            errors.append(f"Invalid price: {data['price']}")
        
        # Validate volume
        try:
            volume = int(data['volume'])
            if volume < MIN_VOLUME:
                errors.append(f"Invalid volume: {volume}")
        except (ValueError, TypeError):
            errors.append(f"Non-numeric volume: {data['volume']}")
        
        # Validate symbol
        if not isinstance(data['symbol'], str) or len(data['symbol']) == 0:
            errors.append(f"Invalid symbol: {data['symbol']}")
        
        if data['price'] == 0:
            errors.append("Zero price - possible collection error")
        
        is_valid = len(errors) == 0
        
        if not is_valid:
            self.logger.warning(f"Validation failed for {data.get('symbol', 'UNKNOWN')}: {errors}")
        
        return is_valid, errors
