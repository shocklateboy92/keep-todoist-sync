from datetime import datetime
import json
import logging
from time import sleep
from typing import Dict, List

import gkeepapi


from .secrets import State, read_secret, read_state, write_state
from .models import Auth, Cache

POLLING_INTERVAL_SECS = 60
CUTOFF_TIME = datetime.fromisoformat("2022-09-20")

logging.basicConfig(level=logging.INFO)
logging.info("Starting...")

google_username = read_secret("google_username")
google_password = read_secret("google_password")

keep = gkeepapi.Keep()

auth = read_state(State.Auth)
if not auth:
    keep.login(google_username, google_password, sync=False)
    token: str = keep.getMasterToken()

    write_state(State.Auth, token)
else:
    keep.resume(google_username, auth, sync=False)

google_state = read_state(State.GoogleTasks)
if google_state:
    keep.restore(json.loads(google_state))


while True:
    logging.info("Beginning sync...")
    keep.sync()
    logging.info("Writing state to file...")
    write_state(State.GoogleTasks, json.dumps(keep.dump()))
    logging.info("Completed sync.")

    tasks: List[gkeepapi._node.TopLevelNode] = keep.all()
    logging.info(f"Found {len(tasks)} tasks in Google Keep")

    after_cutoff = [
        task
        for task in tasks
        if (task.timestamps.edited or task.timestamps.created) > CUTOFF_TIME
    ]
    logging.info(f"Found {len(after_cutoff)} tasks after cutoff date")

    logging.info(
        "Completed iteration. Waiting %s secs before next run", POLLING_INTERVAL_SECS
    )
    sleep(POLLING_INTERVAL_SECS)
