import logging
from time import sleep


POLLING_INTERVAL_SECS = 60

logging.basicConfig(level=logging.INFO)
logging.info("Starting...")

while True:
    logging.info(
        "Completed iteration. Waiting %s secs before next run", POLLING_INTERVAL_SECS
    )
    sleep(POLLING_INTERVAL_SECS)
