from enum import Enum
import logging
from typing import TypeVar

T = TypeVar("T")


class State(Enum):
    Auth = "google_auth"
    GoogleTasks = "google_tasks"
    TaskMap = "task_map"


def get_state_path(name: State):
    return f"/run/app_state/{name.value}.json"


def read_secret(name: str) -> str:
    try:
        with open(f"/run/app_secrets/{name}.txt", mode="r") as file:
            return file.read().strip()
    except FileNotFoundError as e:
        logging.fatal(
            "Unable to read secret '%s'. Make sure it's in the `config` directory next to the docker-compose file",
            name,
        )
        raise e


def read_state(name: State) -> str | None:
    try:
        with open(get_state_path(name), "r") as file:
            return file.read().strip()
    except Exception as e:
        logging.warn(f"Failed to read cached {name.name} state data: {e}")
        return None


def write_state(name: State, value: str) -> None:
    try:
        with open(get_state_path(name), "w") as file:
            file.write(value)
    except Exception as e:
        logging.exception(e)
