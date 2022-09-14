from dataclasses import dataclass

from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)


@dataclass
class LoginResponse:
    name: str
    access_token: str
    refresh_token: str
