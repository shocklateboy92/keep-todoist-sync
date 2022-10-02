import json
import logging
from types import SimpleNamespace
from typing import Any, Type, TypeVar

T = TypeVar("T")

DOCKER_SECRET_MOUNT_PATH = "/run/secrets/"


def get_state_path(type: Type[Any]):
    return f"/run/app_state/{type.__name__.lower()}.json"


def read_secret(name: str) -> str:
    try:
        with open(DOCKER_SECRET_MOUNT_PATH + name, mode="r") as file:
            return file.read().strip()
    except FileNotFoundError:
        logging.fatal("Unable to read docker secret '%s'", name)
        raise SystemExit


def read_state(type: Type[T]) -> T | None:
    try:
        with open(get_state_path(type), "r") as file:
            return json.load(file, object_hook=lambda d: SimpleNamespace(**d))
    except Exception as e:
        logging.warn("Failed to read cached %s state data: %s", type.__name__, e)
        return None


def write_state(value: object) -> None:
    try:
        with open(get_state_path(type(value)), "w") as file:
            json.dump(value.__dict__, file)
    except Exception as e:
        logging.exception(e)
