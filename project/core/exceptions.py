from dataclasses import dataclass


@dataclass
class ApplicationException(Exception):
    body: dict
    code_status: int
