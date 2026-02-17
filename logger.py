import os
import logging

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

logging.basicConfig(
    filename="logs/system.log",
    level=logging.INFO,
    format=LOG_FORMAT
)

def get_logger(name):
    return logging.getLogger(name)
