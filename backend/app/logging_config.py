import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, 'app.log')

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5),
            logging.StreamHandler()
        ]
    )

    logging.info(f"Logging initialized. Writing to: {log_file}")