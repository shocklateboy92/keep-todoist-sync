from datetime import datetime
import json
import logging
from time import sleep
from typing import Dict, List

import gkeepapi
from todoist_api_python.api import TodoistAPI


from .secrets import State, read_secret, read_state, write_state
from .models import Auth, Cache

POLLING_INTERVAL_SECS = 60
CUTOFF_TIME = datetime.fromisoformat("2022-09-20")

logging.basicConfig(level=logging.INFO)
logging.info("Starting...")

google_username = read_secret("google_username")
google_password = read_secret("google_password")
todoist_token = read_secret("todoist_token")

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

todoist = TodoistAPI(todoist_token)

task_map_str = read_state(State.TaskMap)
task_map: Dict[str, str] = json.loads(task_map_str) if task_map_str else {}

logging.debug("Read task map:")
logging.debug(task_map)

while True:
    logging.info("Beginning sync...")
    keep.sync()
    logging.info("Writing state to file...")
    write_state(State.GoogleTasks, json.dumps(keep.dump()))
    logging.info("Completed sync.")

    notes: List[gkeepapi._node.TopLevelNode] = keep.all()
    logging.info(f"Found {len(notes)} notes in Google Keep")

    after_cutoff = [
        note
        for note in notes
        if (note.timestamps.edited or note.timestamps.created) > CUTOFF_TIME
    ]
    logging.info(f"Found {len(after_cutoff)} notes after cutoff date")

    without_maps = [note for note in after_cutoff if not note.id in task_map]
    logging.info(f"Found {len(without_maps)} notes without corresponding todoist tasks")

    for note in without_maps:
        logging.info(
            f"Creating todoist task for note {note.id} with text '{note.text}'"
        )
        try:
            task = todoist.add_task(labels=["google_keep"], content=note.text)
            task_map[note.id] = task.id
            write_state(State.TaskMap, json.dumps(task_map))
        except Exception as e:
            logging.exception(f"Error while creating todoist task: \n {e}")
        logging.info(f"Succesfully created task with id {note.id}.")

    logging.info(
        "Completed iteration. Waiting %s secs before next run", POLLING_INTERVAL_SECS
    )
    sleep(POLLING_INTERVAL_SECS)
