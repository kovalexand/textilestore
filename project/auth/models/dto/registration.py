from dataclasses import dataclass

from pydantic import BaseModel, Field, EmailStr


class RegistrationRequest(BaseModel):
    name: str = Field(min_length=1, max_length=15)
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)


@dataclass
class RegistrationResponse:
    name: str
