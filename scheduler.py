import schedule
import time
import logging
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import StockDataPipeline
from src.utils import setup_logging


def run_scheduled_pipeline():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting scheduled run...")
    
    try:
        pipeline = StockDataPipeline()
        pipeline.run()
    except Exception as e:
        logging.error(f"Scheduled execution failed: {e}")
        print(f"Error: {e}")
    
    print(f"Next execution tomorrow at 18:00\n")


if __name__ == "__main__":
    setup_logging()
    
    print("Stock Data Pipeline Scheduler")
    print("Running daily at 18:00. Press Ctrl+C to stop.\n")
    
    # Run immediately on start
    run_scheduled_pipeline()
    
    # Schedule daily at 18:00 (after market close)
    schedule.every().day.at("18:00").do(run_scheduled_pipeline)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")