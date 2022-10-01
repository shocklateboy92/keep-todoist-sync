import logging
from time import sleep

import gkeepapi  # type: ignore


from .secrets import read_secret, read_state, write_state
from .models import Auth

POLLING_INTERVAL_SECS = 60

logging.basicConfig(level=logging.INFO)
logging.info("Starting...")

google_username = read_secret("google_username")
google_password = read_secret("google_password")

keep = gkeepapi.Keep()

auth = read_state(Auth)
if not auth:
    # keep.login(google_username, google_password)
    # token: str = keep.getMasterToken()
    token = "foo"
    auth = Auth(token)

    write_state(auth)

while True:
    logging.info(
        "Completed iteration. Waiting %s secs before next run", POLLING_INTERVAL_SECS
    )
    sleep(POLLING_INTERVAL_SECS)
