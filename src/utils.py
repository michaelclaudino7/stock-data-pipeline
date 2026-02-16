import logging
import sys
from src.config import LOG_FILE, LOG_FORMAT, LOG_LEVEL


def setup_logging():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    formatter = logging.Formatter(LOG_FORMAT)
    
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        handlers=[file_handler, console_handler]
    )


def send_alert(message):
    logger = logging.getLogger(__name__)
    logger.error(f"ALERT: {message}")
    
    alert_file = LOG_FILE.replace('pipeline.log', 'alerts.log')
    with open(alert_file, 'a') as f:
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")
