import logging
from signal import pause

DOCKER_SECRET_MOUNT_PATH = "/run/secrets/"


def read_secret(name: str):
    try:
        with open(DOCKER_SECRET_MOUNT_PATH + name, mode="r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pause()
        logging.fatal('Unable to read docker secret "%s"', name)
        raise SystemExit
