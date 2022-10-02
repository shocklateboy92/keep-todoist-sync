import logging
from time import sleep

import gkeepapi


from .secrets import read_secret, read_state, write_state
from .models import Auth, Cache

POLLING_INTERVAL_SECS = 60

logging.basicConfig(level=logging.INFO)
logging.info("Starting...")

google_username = read_secret("google_username")
google_password = read_secret("google_password")

keep = gkeepapi.Keep()

auth = read_state(Auth)
if not auth:
    keep.login(google_username, google_password, sync=False)
    token: str = keep.getMasterToken()
    auth = Auth(master_token=token)

    write_state(auth)
else:
    keep.resume(google_username, auth.master_token, sync=False)

state = read_state(Cache)
if state:
    keep.restore(state=state.state)


while True:
    logging.info("Beginning sync...")
    keep.sync()
    logging.info("Writing state to file...")
    write_state(Cache(state=keep.dump()))
    logging.info("Completed sync.")

    tasks = keep.all()
    logging.info("Found %n tasks in Google Keep", len(tasks))

    logging.info(
        "Completed iteration. Waiting %s secs before next run", POLLING_INTERVAL_SECS
    )
    sleep(POLLING_INTERVAL_SECS)
