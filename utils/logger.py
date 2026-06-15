import os
import logging
from datetime import datetime


def setup_logger():
    relative_path = './logs/'
    absolute_path = os.path.abspath(relative_path)

    os.makedirs(absolute_path, exist_ok=True)

    log_file = os.path.join(absolute_path, f"test_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        # filemode="a",  # Append mode
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger()
    return logger
