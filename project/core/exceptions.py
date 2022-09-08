from dataclasses import dataclass
from typing import Any


@dataclass
class ApplicationException(Exception):
    body: dict | Any
    code_status: int
