import logging
from time import sleep

from secrets import read_secret

POLLING_INTERVAL_SECS = 60

logging.basicConfig(level=logging.INFO)
logging.info("Starting...")

google_username = read_secret("google_username")
google_password = read_secret("google_password")

while True:
    logging.info(
        "Completed iteration. Waiting %s secs before next run", POLLING_INTERVAL_SECS
    )
    sleep(POLLING_INTERVAL_SECS)
