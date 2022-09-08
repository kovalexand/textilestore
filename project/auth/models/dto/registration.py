from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class RegistrationRequest(BaseModel):
    name: str
    email: str
    password: str


@dataclass
class RegistrationResponse(BaseModel):
    name: str
