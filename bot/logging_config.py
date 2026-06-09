import logging
import os
from datetime import datetime

IS_SERVERLESS = os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME")


def setup_logging():
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    log_file = None

    if not IS_SERVERLESS:
        try:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"trading_bot_{timestamp}.log")
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except OSError:
            pass

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    return log_file
