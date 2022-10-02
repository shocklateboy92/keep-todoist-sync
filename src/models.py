from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Auth:
    master_token: str


@dataclass
class Cache:
    state: Dict[Any, Any]
