import logging
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    # format="%(asctime)s [%(levelname)s] %(message)s",
    format="",
    handlers=[
        logging.FileHandler(f"log/orginal{datetime.now()}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

