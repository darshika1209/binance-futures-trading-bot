import logging
import os
from datetime import datetime


def setup_logger(name: str = "trading_bot") -> logging.Logger:
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    log_filename = os.path.join(
        logs_dir, f"trading_bot_{datetime.now().strftime('%Y%m%d')}.log"
    )

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
