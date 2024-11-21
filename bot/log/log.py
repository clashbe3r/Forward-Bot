"""
- This script is responsible for keeping logs of activities
"""

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename="bot/log/bot_logs.log")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(filename)s | %(lineno)d |%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
