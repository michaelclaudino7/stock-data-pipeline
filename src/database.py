import psycopg2
import logging
import os


class Database:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.conn = None
        self.connect()
    
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'stock_market'),
                user=os.getenv('DB_USER', 'stockuser'),
                password=os.getenv('DB_PASSWORD', 'stockpass')
            )
            self.logger.info("Database connected")
        except Exception as e:
            self.logger.error(f"Database connection failed: {e}")
            raise
    
    def insert_stock_price(self, data):
        try:
            cursor = self.conn.cursor()
            
            # Insert stock if not exists
            cursor.execute("""
                INSERT INTO stocks (symbol, name) 
                VALUES (%s, %s)
                ON CONFLICT (symbol) DO NOTHING
            """, (data['symbol'], data['symbol']))
            
            # Insert price data
            cursor.execute("""
                INSERT INTO stock_prices 
                (symbol, timestamp, price, volume, latest_trading_day, 
                 previous_close, change, change_percent)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['symbol'],
                data['timestamp'],
                data['price'],
                data['volume'],
                data['latest_trading_day'],
                data['previous_close'],
                data['change'],
                data['change_percent']
            ))
            
            self.conn.commit()
            self.logger.info(f"Data saved to database for {data['symbol']}")
            
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"Failed to insert data: {e}")
            raise
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed")