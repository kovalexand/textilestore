from dataclasses import dataclass


@dataclass
class Token:
    access: str
    refresh: str
