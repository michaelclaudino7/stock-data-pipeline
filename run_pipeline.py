#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import StockDataPipeline
from src.utils import setup_logging

if __name__ == "__main__":
    setup_logging()
    pipeline = StockDataPipeline()
    pipeline.run()
