import logging
import os

def configure_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logger = logging.getLogger()
    logger.setLevel(log_level)

    if logger.handlers:
        return

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

def get_logger(name: str):
    configure_logging()
    return logging.getLogger(name)